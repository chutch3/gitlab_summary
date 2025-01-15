import gitlab
import structlog
from typing import List, Optional
from gitlab_summary.data_models import MergeRequestData
from gitlab_summary.event_processor import GitLabEventProcessor

logger = structlog.get_logger()


class GitLabClient:
    """
    Handles GitLab API interactions and data retrieval.
    """

    def __init__(self, base_url: str, private_token: str, group_id: str = None):
        self._gl = gitlab.Gitlab(url=base_url, private_token=private_token)
        self._gl.auth()
        self._group_id = group_id
        self._event_processor = GitLabEventProcessor()
        logger.info("GitLabClient initialized", base_url=base_url, group_id=group_id)

    def fetch_user_activity(
        self, username: str, date_start: str = None, date_end: str = None
    ) -> List[MergeRequestData]:
        """
        Fetch and process user activity from GitLab
        """
        user = self._get_user(username)
        if not user:
            return []

        events = self._fetch_events(date_start, date_end)
        activities = self._event_processor.process_events(events, username)

        # Fetch MR descriptions for MR-type activities
        for activity in activities:
            if activity.title.startswith("MR Merged"):
                mr_iid = int(activity.title.split()[-1].strip(")"))
                activity.description = (
                    self._fetch_mr_description(activity.project_id, mr_iid) or ""
                )

        return activities

    def _get_user(self, username: str) -> Optional[dict]:
        """Fetch user information from GitLab"""
        users = self._gl.users.list(username=username)
        if not users:
            logger.warning("No user found matching username", username=username)
            return None
        return users[0]

    def _fetch_events(self, date_start: str = None, date_end: str = None) -> List[dict]:
        """Fetch all events matching the given criteria"""
        event_filters = {}
        if date_start:
            event_filters["after"] = date_start
        if date_end:
            event_filters["before"] = date_end

        all_events = []
        page = 1
        while True:
            events = self._gl.events.list(page=page, per_page=100, **event_filters)
            if not events:
                break
            all_events.extend(events)
            page += 1

        return all_events

    def _fetch_mr_description(self, project_id: int, mr_iid: int) -> str:
        """Fetch a single merge request's description"""
        try:
            project = self._gl.projects.get(project_id)
            merge_req = project.mergerequests.get(mr_iid)
            return merge_req.description
        except Exception as e:
            logger.warning(
                "Failed to fetch MR description",
                project_id=project_id,
                mr_iid=mr_iid,
                error=str(e),
            )
            return ""
