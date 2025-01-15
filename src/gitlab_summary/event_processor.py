from datetime import datetime
import structlog
from typing import Dict, Tuple, List
from gitlab_summary.data_models import MergeRequestData

logger = structlog.get_logger()


class GitLabEventProcessor:
    """
    Processes GitLab events and converts them into weighted activity data.
    Handles the business logic of event processing and weight calculations.
    """

    def __init__(self):
        self.now = datetime.now()

    def calculate_weight(self, event_time: datetime) -> float:
        """
        Calculate weight based on how recent the event is.
        Returns a value between 1.0 and 2.0, where:
        - Most recent events get weight close to 2.0
        - Oldest events get weight close to 1.0
        """
        return 1.0 + (
            1.0
            - (self.now.astimezone(event_time.tzinfo) - event_time).total_seconds()
            / 86400
        )

    def process_events(
        self, events: List[dict], username: str
    ) -> List[MergeRequestData]:
        """
        Process a list of GitLab events into weighted MergeRequestData objects
        """
        mr_data_dict: Dict[Tuple[int, int], MergeRequestData] = {}

        for event in events:
            event_time = datetime.fromisoformat(event.attributes.get("created_at"))
            weight = self.calculate_weight(event_time)

            processed_data = self._process_single_event(
                event, username, weight, event_time
            )
            if processed_data:
                key, data = processed_data
                mr_data_dict[key] = data

        result = list(mr_data_dict.values())
        result.sort(
            key=lambda x: x.timestamp if x.timestamp else datetime.min, reverse=True
        )
        return result

    def _process_single_event(
        self, event: dict, username: str, weight: float, event_time: datetime
    ) -> Tuple[Tuple[int, int], MergeRequestData]:
        """
        Process a single event and return a tuple of (key, MergeRequestData)
        """
        action_name = event.attributes.get("action_name")
        project_id = event.attributes.get("project_id")

        if "opened" in action_name:
            return self._process_mr_event(event, username, weight, event_time)
        elif "pushed" in action_name:
            return self._process_push_event(event, username, weight, event_time)
        elif "commented" in action_name:
            return self._process_comment_event(event, username, weight, event_time)

        return None

    def _process_mr_event(self, event, username, weight, event_time):
        project_id = event.attributes.get("project_id")
        merge_req_id = event.attributes.get("target_id")
        merge_req_iid = event.attributes.get("target_iid")

        if merge_req_id is None or project_id is None:
            return None

        logger.info(
            f"Processing MR merge event: {event.attributes.get('target_title')}, {weight}"
        )

        return (project_id, merge_req_id), MergeRequestData(
            title=f"MR Merged (IID {merge_req_iid})",
            description="",  # Description will be fetched by GitLabClient
            author=username,
            commits=[],
            comments=[],
            weight=weight,
            timestamp=event_time,
        )

    def _process_push_event(self, event, username, weight, event_time):
        project_id = event.attributes.get("project_id")
        push_data = event.attributes.get("push_data") or {}
        commit_title = push_data.get("commit_title", "")

        if not commit_title or project_id is None:
            return None

        logger.info(f"Processing commit push event: {commit_title}, {weight}")
        return (project_id, hash(commit_title)), MergeRequestData(
            title="Commit Pushed",
            description=commit_title,
            author=username,
            commits=[],
            comments=[],
            weight=weight,
            timestamp=event_time,
        )

    def _process_comment_event(self, event, username, weight, event_time):
        project_id = event.attributes.get("project_id")
        note = event.attributes.get("note")

        if not note:
            return None

        logger.info(f"Processing note event: {note.get('body')}, {weight}")
        return (project_id, note.get("id")), MergeRequestData(
            title="Note",
            description=note.get("body"),
            author=username,
            commits=[],
            comments=[],
            weight=weight,
            timestamp=event_time,
        )
