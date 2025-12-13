from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class CompanyInsightRequest(BaseModel):
    company: str = Field(..., min_length=2, description="Company to analyze.")
    location: str | None = Field(
        default=None, description="Optional city, state, or region."
    )
    role: str | None = Field(
        default=None,
        description="Role, department, or perspective to focus on (e.g. engineering).",
    )
    focus_areas: list[str] = Field(
        default_factory=list,
        description="Specific culture or policy areas to explore.",
    )
    metrics_of_interest: list[str] = Field(
        default_factory=list,
        description="Key metrics (attrition, promotion, pay equity, etc.)",
    )
    model: str | None = Field(
        default=None,
        description="Override the default OpenAI model configured on the server.",
    )
    temperature: float = Field(
        default=0.4,
        ge=0,
        le=2,
        description="Sampling temperature for creative vs. focused answers.",
    )
    language: str | None = Field(
        default=None,
        description="Language to respond with. Defaults to English.",
    )
    max_highlights: int = Field(
        default=3,
        ge=1,
        le=6,
        description="How many highlights/risks/actions to request from the model.",
    )


class CompanyInsightResponse(BaseModel):
    company: str
    model: str
    summary: str
    positives: list[str] = Field(default_factory=list)
    concerns: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
    usage: dict[str, int] | None = Field(
        default=None,
        description="Token usage or billing metadata provided by the model.",
    )
    raw: dict[str, Any] | None = Field(
        default=None,
        description="Raw payload returned by the provider for debugging.",
    )
