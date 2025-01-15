import pytest
from gitlab_summary.summary_generator import build_prompt, generate_linkedin_summary
from gitlab_summary.data_models import MergeRequestData
from gitlab_summary.openai_client import OpenAIClient


def test_build_prompt():
    mr_data = MergeRequestData(
        title="Add feature X",
        description="Implements feature X.",
        author="tester",
        commits=["Initial commit"],
        comments=["Looks good!"],
    )
    prompt = build_prompt([mr_data])
    assert "Add feature X" in prompt
    assert "Implements feature X." in prompt


@pytest.mark.integration
def test_generate_linkedin_summary():
    openai_client = OpenAIClient(api_key="DUMMY_FOR_TEST")  # Replace with real key
    mr_data = MergeRequestData(
        title="Add feature X",
        description="Implements feature X.",
        author="tester",
        commits=["Initial commit"],
        comments=["Looks good!"],
    )
    summary = generate_linkedin_summary(openai_client, [mr_data])
    assert isinstance(summary, str)
    assert len(summary) > 0
