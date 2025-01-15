"""
CLI entry point for GitLab summary generation.
"""

import sys
import structlog
import typer
from typing import Optional
from datetime import datetime
from gitlab_summary.config import load_config
from gitlab_summary.logging_setup import configure_logging
from gitlab_summary.gitlab_client import GitLabClient
from gitlab_summary.openai_client import OpenAIClient
from gitlab_summary.summary_generator import generate_linkedin_summary

logger = structlog.get_logger()

app = typer.Typer(help="Generate LinkedIn summaries from GitLab activity.")


@app.command()
def main(
    username: str = typer.Argument(..., help="GitLab username to fetch activity for"),
    start_date: Optional[datetime] = typer.Option(
        None,
        "--start-date",
        "-s",
        formats=["%Y-%m-%d"],
        help="Start date for activity range (YYYY-MM-DD)",
    ),
    end_date: Optional[datetime] = typer.Option(
        None,
        "--end-date",
        "-e",
        formats=["%Y-%m-%d"],
        help="End date for activity range (YYYY-MM-DD)",
    ),
    output_file: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path for the summary (defaults to stdout)",
    ),
):
    """
    Generate a LinkedIn-ready summary of GitLab activity.

    This tool fetches a user's GitLab activity (merge requests, commits, etc.)
    and uses OpenAI to generate a professional summary suitable for LinkedIn.
    """
    config = load_config()
    configure_logging(config.LOG_LEVEL)

    try:
        logger.info("Starting GitLab summary tool", username=username)

        # Initialize clients
        gl_client = GitLabClient(
            config.GITLAB_URL, config.GITLAB_TOKEN, group_id=config.GITLAB_GROUP_ID
        )
        openai_client = OpenAIClient(config.OPENAI_API_KEY)

        # Convert dates to strings if provided
        date_start = start_date.strftime("%Y-%m-%d") if start_date else None
        date_end = end_date.strftime("%Y-%m-%d") if end_date else None

        # Fetch activity data
        activities = gl_client.fetch_user_activity(
            username, date_start=date_start, date_end=date_end
        )

        if not activities:
            logger.warning("No activities found for user", username=username)
            raise typer.Exit(1)

        # Generate summary
        summary_text = generate_linkedin_summary(openai_client, activities)

        # Output handling
        if output_file:
            try:
                with open(output_file, "w") as f:
                    f.write(summary_text)
                logger.info("Summary written to file", file=output_file)
            except Exception as e:
                logger.error("Failed to write to file", error=str(e))
                raise typer.Exit(1)
        else:
            typer.echo("===== LINKEDIN SUMMARY =====")
            typer.echo(summary_text)
            typer.echo("============================")

    except Exception as e:
        logger.error("An error occurred", error=str(e))
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
