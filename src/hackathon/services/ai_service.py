import json
import logging
import os
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types

from hackathon.models.schemas import AIReport

load_dotenv()

logger = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

SYSTEM_PROMPT = """Act as a senior software architect. Analyze only the provided \
repository evidence and do not invent information that is not supported by it.

Based solely on the structured repository facts given to you, determine:
- the project's purpose and a concise summary
- its technology stack and architecture
- its key components
- its strengths, weaknesses, and risks
- concrete recommendations

Also produce a list of issues. Each issue must include a severity \
(one of: critical, high, medium, low), a title, the relevant file, the \
evidence from the repository facts that supports it, and a recommendation.

Finally, produce a health_score from 0 to 100 and a concise final_assessment.

Respond with JSON only, matching the provided schema exactly. Do not fabricate \
files, dependencies, or facts that are not present in the evidence."""


class AIServiceError(RuntimeError):
    pass


def generate_report(analysis_result: dict[str, Any]) -> dict[str, Any]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise AIServiceError("GEMINI_API_KEY is not set. Add it to a .env file.")

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=[
                SYSTEM_PROMPT,
                "Repository evidence (structured JSON facts):",
                json.dumps(analysis_result, default=str),
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_json_schema=AIReport.model_json_schema(),
            ),
        )
    except Exception as exc:  # noqa: BLE001 - surfaced as a clean service error
        # The provider message can carry request details, so log it server-side
        # and keep the client-facing error generic.
        logger.exception("Gemini request failed")
        raise AIServiceError("The AI provider request failed.") from exc

    if not response.text:
        raise AIServiceError("Gemini returned an empty response.")

    report = AIReport.model_validate_json(response.text)
    return report.model_dump()
