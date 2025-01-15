import pytest
from gitlab_summary.openai_client import OpenAIClient


@pytest.mark.integration
def test_generate_summary():
    """
    Integration test for OpenAIClient.generate_summary.
    """
    client = OpenAIClient(
        api_key="DUMMY_FOR_TEST"
    )  # Replace with actual environment variable
    prompt = "Write a short test summary."
    summary = client.generate_summary(prompt)
    assert isinstance(summary, str)
    assert len(summary) > 0
