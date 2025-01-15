import openai
import structlog

logger = structlog.get_logger()


class OpenAIClient:
    """
    Client responsible for generating text summaries using OpenAI.
    """

    def __init__(self, api_key: str):
        openai.api_key = api_key
        logger.info("OpenAI client initialized")

    def generate_summary(self, prompt: str) -> str:
        """
        Send the prompt to OpenAI's API and return the generated summary.
        """
        logger.debug("Generating summary with OpenAI", prompt_length=len(prompt))
        try:
            system_prompt = """
            You are a helpful assistant that summarizes GitLab activity for a user into a LinkedIn-ready summary to help them get a job.
            Highlight the user's contributions to the company and their skills. This will be made public, so be careful not to include any sensitive information.
            Using the weights provided, highlight the more recent contributions. 

            Here is a link to documentation on how to write a good LinkedIn experience: 
            <a href="https://www.linkedin.com/pulse/how-write-your-linkedin-experience-section-examples-karen-tisdell/">How to write your LinkedIn experience section: examples</a>
            """
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            summary = response.choices[0].message.content.strip()
            logger.debug("Summary received", summary_length=len(summary))
            return summary
        except Exception as e:
            logger.error("OpenAI request failed", error=str(e))
            raise
