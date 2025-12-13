from fastapi import APIRouter, HTTPException, status

from app.api.schemas.ask_openai import (
    CompanyInsightRequest,
    CompanyInsightResponse,
)
from app.integrations import (
    OpenAIIntegrationError,
    generate_company_insight,
)

router = APIRouter()


@router.post(
    "/",
    response_model=CompanyInsightResponse,
    summary="Get a structured opinion about a company using OpenAI.",
)
def ask_openai_for_company_opinion(
    payload: CompanyInsightRequest,
) -> CompanyInsightResponse:
    try:
        return generate_company_insight(payload)
    except OpenAIIntegrationError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc
