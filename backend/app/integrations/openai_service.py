from __future__ import annotations

import json
from functools import lru_cache
from textwrap import dedent
from typing import Any, Iterable

from openai import OpenAI, OpenAIError

from app.api.schemas.ask_openai import (
    CompanyInsightRequest,
    CompanyInsightResponse,
)
from app.settings import settings

DEFAULT_FOCUS_AREAS = [
    "overall employee sentiment",
    "compensation and benefits",
    "management transparency",
    "growth and learning opportunities",
]

DEFAULT_METRICS = [
    "attrition risk",
    "promotion velocity",
    "DEI progress",
    "work-life balance",
]


class OpenAIIntegrationError(RuntimeError):
    """Raised when the OpenAI integration fails or returns invalid data."""


@lru_cache
def _get_client() -> OpenAI:
    api_key = settings.open_ai_api_key
    if not api_key or api_key == "OPEN_AI_API_KEY":
        raise OpenAIIntegrationError(
            "OpenAI API key is not configured. "
            "Set OPEN_AI_API_KEY or update the settings file.",
        )

    return OpenAI(
        api_key=api_key,
        base_url=settings.open_ai_base_url,
        organization=settings.open_ai_organization,
    )


def generate_company_insight(
    payload: CompanyInsightRequest,
) -> CompanyInsightResponse:
    client = _get_client()
    messages = _build_messages(payload)
    model = payload.model or settings.open_ai_default_model

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=payload.temperature,
            response_format={"type": "json_object"},
        )
    except OpenAIError as exc:
        raise OpenAIIntegrationError(
            "OpenAI rejected the request or is unavailable right now.",
        ) from exc

    content = _extract_content(completion)
    structured = _parse_structured_response(content)

    usage = None
    if getattr(completion, "usage", None):
        usage = {
            "prompt_tokens": getattr(completion.usage, "prompt_tokens", None),
            "completion_tokens": getattr(completion.usage, "completion_tokens", None),
            "total_tokens": getattr(completion.usage, "total_tokens", None),
        }

    return CompanyInsightResponse(
        company=payload.company,
        model=completion.model or model,
        summary=structured.get("summary", "").strip(),
        positives=_coerce_list(structured.get("positives")),
        concerns=_coerce_list(structured.get("concerns")),
        recommended_actions=_coerce_list(structured.get("recommended_actions")),
        usage=usage,
        raw={
            "response_id": getattr(completion, "id", None),
            "created": getattr(completion, "created", None),
            "system_fingerprint": getattr(completion, "system_fingerprint", None),
        },
    )


def _build_messages(payload: CompanyInsightRequest) -> list[dict[str, str]]:
    focus = payload.focus_areas or DEFAULT_FOCUS_AREAS
    metrics = payload.metrics_of_interest or DEFAULT_METRICS
    highlights = payload.max_highlights

    focus_block = "\n".join(f"- {item}" for item in focus)
    metrics_block = "\n".join(f"- {item}" for item in metrics)

    prompt = dedent(
        f"""
        Company: {payload.company}
        Location context: {payload.location or "Global/unspecified"}
        Perspective: {payload.role or "All employee groups"}

        Focus areas:
        {focus_block}

        Metrics of interest:
        {metrics_block}

        Respond in {payload.language or "English"} with valid JSON containing:
        - summary: 3 sentence narrative.
        - positives: up to {highlights} bullets with the biggest strengths.
        - concerns: up to {highlights} bullets with risks or warning signs.
        - recommended_actions: up to {highlights} actions a candidate should take.

        Be specific, cite signals (e.g. layoffs, investor notes) when available,
        and keep each bullet under 30 words.
        """
    ).strip()

    return [
        {
            "role": "system",
            "content": (
                "You are a meticulous career research assistant. "
                "You combine verified market knowledge, recent news, and employee "
                "signals to brief job seekers."
            ),
        },
        {"role": "user", "content": prompt},
    ]


def _extract_content(completion: Any) -> str:
    try:
        choice = completion.choices[0]
        content = choice.message.content
    except (AttributeError, IndexError, KeyError) as exc:
        raise OpenAIIntegrationError(
            "OpenAI response did not include any choices.",
        ) from exc

    if isinstance(content, str):
        return content

    if isinstance(content, Iterable):
        text_fragments: list[str] = []
        for fragment in content:
            if isinstance(fragment, str):
                text_fragments.append(fragment)
                continue
            text_value = getattr(fragment, "text", None)
            if text_value:
                if isinstance(text_value, str):
                    text_fragments.append(text_value)
                else:
                    text_fragments.append(getattr(text_value, "value", ""))
        combined = "".join(text_fragments).strip()
        if combined:
            return combined

    raise OpenAIIntegrationError("Unable to extract textual content from OpenAI reply.")


def _parse_structured_response(content: str) -> dict[str, Any]:
    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        raise OpenAIIntegrationError(
            "OpenAI returned an invalid JSON payload.",
        ) from exc


def _coerce_list(value: Any) -> list[str]:
    if not value:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    return [str(value)]
