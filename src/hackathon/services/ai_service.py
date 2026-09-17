import json
import logging
import os
from copy import deepcopy
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from groq import Groq
from pydantic import ValidationError

from hackathon.models.schemas import AIReport


ROOT_DIR = Path(__file__).resolve().parents[3]
load_dotenv(ROOT_DIR / ".env")

logger = logging.getLogger(__name__)

PRIMARY_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b",
)

MODELS = list(
    dict.fromkeys(
        [
            PRIMARY_MODEL,
            "qwen/qwen3.8-27b",
            "openai/gpt-oss-20b",
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

Do not fabricate files, dependencies, technologies, frameworks,
functions, classes, tests, or repository facts.

Keep the response concise and evidence-based.

Maximum:
- 4 strengths
- 4 weaknesses
- 5 risks
- 5 recommendations
- 6 issues
"""


class AIServiceError(RuntimeError):
    pass


def _make_strict_schema(
    schema: dict[str, Any],
) -> dict[str, Any]:

    schema = deepcopy(schema)

    def process(value: Any) -> None:
        if isinstance(value, dict):

            if value.get("type") == "object":
                value["additionalProperties"] = False

                properties = value.get("properties")

                if isinstance(properties, dict):
                    value["required"] = list(
                        properties.keys()
                    )

            for child in value.values():
                process(child)

        elif isinstance(value, list):
            for child in value:
                process(child)

    process(schema)

    return schema


def _is_retryable_error(
    exc: Exception,
) -> bool:

    message = str(exc).lower()

    return (
        "429" in message
        or "rate limit" in message
        or "rate_limit" in message
        or "500" in message
        or "502" in message
        or "503" in message
        or "504" in message
        or "unavailable" in message
        or "overloaded" in message
    )


def generate_report(
    analysis_result: dict[str, Any],
) -> dict[str, Any]:

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise AIServiceError(
            "GROQ_API_KEY is not set. "
            "Add it to the project .env file."
        )

    repository_json = json.dumps(
        analysis_result,
        default=str,
        ensure_ascii=False,
    )

    if not repository_json.strip():
        raise AIServiceError(
            "Repository analysis is empty."
        )

    client = Groq(
        api_key=api_key
    )

    schema = _make_strict_schema(
        AIReport.model_json_schema()
    )

    response = None
    last_error = None

    for model in MODELS:

        try:
            logger.info(
                "Trying Groq model: %s",
                model,
            )

            response = (
                client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": (
                                SYSTEM_PROMPT
                                + "\n\n"
                                + "Repository evidence:\n"
                                + repository_json
                            ),
                        }
                    ],
                    reasoning_effort="low",
                    response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "name": "codescope_ai_report",
                            "strict": True,
                            "schema": schema,
                        },
                    },
                )
            )

            logger.info(
                "Groq model succeeded: %s",
                model,
            )

            break

        except Exception as exc:
            last_error = exc

            logger.warning(
                "Groq model %s failed: %s",
                model,
                exc,
            )

            if _is_retryable_error(exc):
                continue

            logger.exception(
                "Groq request failed"
            )

            raise AIServiceError(
                "The AI provider request failed."
            ) from exc

    if response is None:
        logger.error(
            "All configured Groq models failed."
        )

        raise AIServiceError(
            "All AI models are currently unavailable."
        ) from last_error

    try:
        content = (
            response
            .choices[0]
            .message
            .content
        )

    except Exception as exc:
        raise AIServiceError(
            "The AI provider returned "
            "an unexpected response."
        ) from exc

    if not content:
        raise AIServiceError(
            "The AI provider returned "
            "an empty response."
        )

    try:
        data = json.loads(content)

        report = AIReport.model_validate(
            data
        )

    except json.JSONDecodeError as exc:
        logger.exception(
            "Groq returned invalid JSON."
        )

        raise AIServiceError(
            "The AI provider returned "
            "invalid JSON."
        ) from exc

    except ValidationError as exc:
        logger.exception(
            "Groq response does not "
            "match AIReport."
        )

        raise AIServiceError(
            "The AI provider returned "
            "an invalid response."
        ) from exc

    except Exception as exc:
        logger.exception(
            "Failed to parse Groq response."
        )

        raise AIServiceError(
            "The AI provider returned "
            "an invalid response."
        ) from exc

    return report.model_dump()