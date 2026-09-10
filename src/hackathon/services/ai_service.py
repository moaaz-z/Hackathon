import json
import logging
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from hackathon.models.schemas import AIReport


load_dotenv()

logger = logging.getLogger(__name__)

MODEL = "gemini-3.6-flash"
BASE_URL = "https://backend.sovereigneg.com/v1"


SYSTEM_PROMPT = """Act as a senior software architect.

Analyze only the provided repository evidence.
Do not invent information that is not supported by the evidence.

Based solely on the structured repository facts, determine:

- the project's purpose and a concise summary
- its technology stack and architecture
- its key components
- its strengths, weaknesses, and risks
- concrete recommendations

Also produce a list of issues.

Each issue must include:
- severity: critical, high, medium, or low
- title
- relevant file
- evidence from the repository facts
- recommendation

Finally, produce:
- health_score from 0 to 100
- concise final_assessment

Respond with JSON only.
Do not fabricate files, dependencies, or facts that are not present
in the repository evidence.
"""


class AIServiceError(RuntimeError):
    pass


def generate_report(analysis_result: dict[str, Any]) -> dict[str, Any]:
    api_key = os.getenv("SOVEREIGNEG_API_KEY")

    if not api_key:
        raise AIServiceError(
            "SOVEREIGNEG_API_KEY is not set. Add it to your .env file."
        )

    client = OpenAI(
        base_url=BASE_URL,
        api_key=api_key,
    )

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": (
                        "Repository evidence "
                        "(structured JSON facts):\n\n"
                        + json.dumps(analysis_result, default=str)
                    ),
                },
            ],
        )

    except Exception as exc:
        logger.exception("AI request failed")
        raise AIServiceError(
            "The AI provider request failed."
        ) from exc

    content = response.choices[0].message.content

    if not content:
        raise AIServiceError("AI returned an empty response.")

    try:
        report = AIReport.model_validate_json(content)
    except Exception as exc:
        logger.exception("AI returned invalid JSON")
        raise AIServiceError(
            "AI returned an invalid report."
        ) from exc

    return report.model_dump()