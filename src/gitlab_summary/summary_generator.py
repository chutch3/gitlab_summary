import structlog
from typing import List
from gitlab_summary.data_models import MergeRequestData

logger = structlog.get_logger()


def build_prompt(merge_requests: List[MergeRequestData]) -> str:
    """
    Build a prompt for OpenAI using the user's MR details.
    """
    prompt_sections = []
    for mr in merge_requests:
        section = f"Description: {mr.description}\nWeight: {mr.weight}\n----\n"
        prompt_sections.append(section)
    return "\n".join(prompt_sections)


def generate_linkedin_summary(
    openai_client, merge_requests: List[MergeRequestData]
) -> str:
    """
    Generates a LinkedIn-suitable summary from merge requests.
    """
    logger.debug("Generating LinkedIn summary", mr_count=len(merge_requests))
    prompt = build_prompt(merge_requests)
    return openai_client.generate_summary(prompt)
