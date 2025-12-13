# Backend

FastAPI service that powers the Doorlook API. The service exposes a small surface today, but ships with a production-ready OpenAI integration used to generate structured company insights.

## Environment variables

| Variable | Description |
| --- | --- |
| `OPEN_AI_API_KEY` | Required. Secret key used to authenticate with OpenAI. |
| `OPEN_AI_BASE_URL` | Optional. Override the default API URL (useful for Azure/OpenAI proxies). |
| `OPEN_AI_ORGANIZATION` | Optional. Organization used for API usage attribution. |
| `OPEN_AI_DEFAULT_MODEL` | Optional. Default model used by the insight endpoint (defaults to `gpt-4o-mini`). |

Create an `.env` file in `backend/` or export the variables before launching the server.

## Company insight endpoint

`POST /api/v1/ask-openai`

Body:

```json
{
  "company": "Doorlook",
  "location": "Remote",
  "role": "Product",
  "focus_areas": ["culture", "compensation"],
  "metrics_of_interest": ["attrition", "growth"],
  "max_highlights": 3,
  "temperature": 0.3,
  "language": "English"
}
```

The endpoint responds with structured JSON containing a summary, top strengths, risks, recommended actions, token usage, and lightweight metadata about the provider response. Validation is enforced via Pydantic schemas and errors are mapped to 4xx/5xx status codes for observability.

## Running locally

```bash
poetry install
poetry run uvicorn app.main:app --reload
```

Visit `http://localhost:8000/api/swagger` for the interactive API documentation.
