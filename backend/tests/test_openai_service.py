import pytest

from app.integrations.openai_service import (
    _coerce_list,
    _extract_content,
    _parse_structured_response,
    OpenAIIntegrationError,
)


def _make_completion(content):
    message = type("Message", (), {"content": content})
    choice = type("Choice", (), {"message": message})
    return type("Completion", (), {"choices": [choice]})


def test_parse_structured_response_returns_dict():
    content = '{"summary": "Clear", "positives": ["brand"]}'
    parsed = _parse_structured_response(content)

    assert parsed["summary"] == "Clear"
    assert parsed["positives"] == ["brand"]


def test_parse_structured_response_rejects_invalid_payload():
    with pytest.raises(OpenAIIntegrationError):
        _parse_structured_response("not json")


def test_extract_content_accepts_plain_string():
    completion = _make_completion('{"summary":"ok"}')
    assert _extract_content(completion) == '{"summary":"ok"}'


def test_extract_content_concatenates_iterable_parts():
    part_with_text = type("Part", (), {"text": type("Text", (), {"value": "two"})()})
    completion = _make_completion(["one", part_with_text])

    assert _extract_content(completion) == "onetwo"


def test_extract_content_requires_choice():
    completion = type("Completion", (), {"choices": []})

    with pytest.raises(OpenAIIntegrationError):
        _extract_content(completion)


def test_coerce_list_normalizes_values():
    assert _coerce_list([" one ", ""]) == ["one"]
    assert _coerce_list("solo") == ["solo"]
    assert _coerce_list(None) == []
