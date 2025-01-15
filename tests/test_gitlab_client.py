import pytest
from gitlab_summary.gitlab_client import GitLabClient


@pytest.mark.integration
def test_fetch_merge_requests():
    """
    Integration test for GitLabClient.fetch_merge_requests.
    """
    client = GitLabClient(
        base_url="https://gitlab.com",  # Replace with your GITLAB_URL if different
        private_token="DUMMY_FOR_TEST",  # Replace with your GITLAB_TOKEN or rely on environment
    )
    # This will likely fail unless you provide valid auth in real environment.
    # Test demonstrates real calls, no mocks.

    merge_requests = client.fetch_merge_requests("some_user")
    assert isinstance(merge_requests, list)
