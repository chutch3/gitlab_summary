# GitLab Activity Summarizer

A Python tool that converts your GitLab development activity into professional experience descriptions suitable for LinkedIn profiles. It analyzes your merge requests, commits, and comments, prioritizing recent work to generate polished, achievement-focused descriptions of your development experience.

## Core Features

- **Activity Analysis**: Collects and analyzes your GitLab development history
- **Professional Writing**: Uses OpenAI to generate LinkedIn-ready experience descriptions
- **Time-Based Weighting**: Emphasizes recent projects and achievements
- **Achievement Focus**: Highlights impactful contributions and technical skills

## Project Structure

The project is organized into focused components:

### Core Components

- `gitlab_client.py`: Handles GitLab API interactions and data retrieval
- `event_processor.py`: Processes and weights GitLab events based on recency
- `openai_client.py`: Manages OpenAI API interactions for summary generation
- `data_models.py`: Defines data structures used throughout the application

### How It Works

1. The GitLab client fetches user activities through GitLab's Events API
2. The event processor:
   - Converts raw events into structured data
   - Applies time-based weights (newer events get weights closer to 2.0)
   - Sorts activities by recency
3. The OpenAI client generates natural language summaries from the processed data

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd gitlab-activity-summarizer
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

4. Run the script:
```bash
python src/gitlab_summary/main.py <gitlab_user_id>
```


## Configuration

Create a `.env` file in the project root:
```bash
GITLAB_URL=https://gitlab.com
GITLAB_TOKEN=your_gitlab_token
OPENAI_API_KEY=your_openai_api_key
GITLAB_GROUP_ID=your_gitlab_group_id # optional
```
