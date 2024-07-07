from fastapi import APIRouter
from openai import OpenAI

from app.settings import settings

router = APIRouter()


@router.get("/")
def ask_openai_for_company_opinion(
    company: str,
    location: str | None = None,
):
    client = OpenAI(api_key=settings.open_ai_api_key)

    completeions = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a specialist job seeker, and your task is to help a friend with information about the job that they request.",
            },
            {
                "role": "user",
                "content": f"Company name: {company}, Location: {location}",
            },
        ],
    )

    return completeions
