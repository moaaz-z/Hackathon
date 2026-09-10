import json
import logging
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import ValidationError

from hackathon.models.schemas import AIReport


# Load .env from project root
ROOT_DIR = Path(__file__).resolve().parents[3]
load_dotenv(ROOT_DIR / ".env")

logger = logging.getLogger(__name__)


# Primary model comes from .env.
# Other models are used automatically if the primary model returns 503.
PRIMARY_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

MODELS = list(
    dict.fromkeys(
        [
            PRIMARY_MODEL,
            "gemini-3.7-flash",
            "gemini-3.6-flash",
        ]
    )
)


SYSTEM_PROMPT = """
Act as a senior software architect.

Analyze only the provided repository evidence.
Do not invent information that is not supported by the repository.

Determine:
- project purpose
- concise project summary
- technology stack
- architecture
- key components
- strengths
- weaknesses
- risks
- concrete recommendations

For every issue include:
- severity: critical, high, medium, or low
- title
- relevant file
- evidence
- recommendation

Also produce:
- health_score from 0 to 100
- concise final_assessment

Return JSON only and match the provided schema exactly.

Do not fabricate files, dependencies, technologies, or repository facts.
"""


class AIServiceError(RuntimeError):
    """Raised when the AI provider cannot generate a valid report."""

    pass


def _is_temporary_unavailable_error(exc: Exception) -> bool:
    """
    Returns True when Gemini is temporarily unavailable,
    usually because the model is under heavy demand.
    """

    message = str(exc).lower()

    return (
        "503" in message
        or "unavailable" in message
        or "high demand" in message
    )


def generate_report(
    analysis_result: dict[str, Any],
) -> dict[str, Any]:

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise AIServiceError(
            "GEMINI_API_KEY is not set. Add it to the project .env file."
        )

    client = genai.Client(
        api_key=api_key
    )

    repository_json = json.dumps(
        analysis_result,
        default=str,
        ensure_ascii=False,
    )

    response = None
    last_error = None

    # Try primary model, then fallback models
    for model in MODELS:

        try:
            logger.info(
                "Trying Gemini model: %s",
                model
            )

            response = client.models.generate_content(
                model=model,
                contents=[
                    SYSTEM_PROMPT,
                    "Repository evidence:",
                    repository_json,
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_json_schema=AIReport.model_json_schema(),
                ),
            )

            logger.info(
                "Gemini model succeeded: %s",
                model
            )

            break

        except Exception as exc:
            last_error = exc

            logger.warning(
                "Gemini model %s failed: %s",
                model,
                exc,
            )

            # Only fallback when Gemini is temporarily unavailable
            if _is_temporary_unavailable_error(exc):
                continue

            # Authentication, invalid request, etc.
            logger.exception(
                "Gemini request failed"
            )

            raise AIServiceError(
                "The AI provider request failed."
            ) from exc

    # Every model failed
    if response is None:

        logger.error(
            "All configured Gemini models failed."
        )

        raise AIServiceError(
            "All Gemini models are currently unavailable."
        ) from last_error

    # Empty response
    if not response.text:

        raise AIServiceError(
            "Gemini returned an empty response."
        )

    # Validate Gemini JSON against AIReport
    try:
        report = AIReport.model_validate_json(
            response.text
        )

    except ValidationError as exc:

        logger.exception(
            "Gemini returned JSON that does not match AIReport."
        )

        raise AIServiceError(
            "The AI provider returned an invalid response."
        ) from exc

    except Exception as exc:

        logger.exception(
            "Failed to parse Gemini response."
        )

        raise AIServiceError(
            "The AI provider returned an invalid response."
        ) from exc

    return report.model_dump()