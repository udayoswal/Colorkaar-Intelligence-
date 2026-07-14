"""Thin wrapper over the Anthropic API: structured JSON output + prompt caching."""

import json
import os
import time

import anthropic

DEFAULT_MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-4-8")


def get_client() -> anthropic.Anthropic:
    return anthropic.Anthropic()


def structured_call(
    client: anthropic.Anthropic,
    *,
    system: str,
    user: str,
    json_schema: dict,
    model: str | None = None,
    max_tokens: int = 4096,
    max_retries: int = 5,
) -> tuple[dict, anthropic.types.Usage]:
    """One Claude call constrained to json_schema. Returns (parsed_json, usage).

    The system prompt is cache_control-tagged since it's identical across
    every call in a run — the per-lead content lives entirely in `user`.
    """
    last_error: Exception | None = None
    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model=model or DEFAULT_MODEL,
                max_tokens=max_tokens,
                system=[
                    {
                        "type": "text",
                        "text": system,
                        "cache_control": {"type": "ephemeral"},
                    }
                ],
                messages=[{"role": "user", "content": user}],
                output_config={
                    "format": {"type": "json_schema", "schema": json_schema}
                },
            )
        except anthropic.RateLimitError as e:
            last_error = e
            retry_after = int(e.response.headers.get("retry-after", "10"))
            time.sleep(retry_after)
            continue
        except anthropic.APIStatusError as e:
            if e.status_code >= 500:
                last_error = e
                time.sleep(min(2**attempt, 30))
                continue
            raise
        except anthropic.APIConnectionError as e:
            last_error = e
            time.sleep(min(2**attempt, 30))
            continue

        if response.stop_reason == "refusal":
            raise RuntimeError(f"Model refused the request: {response.stop_details}")

        text = next(b.text for b in response.content if b.type == "text")
        return json.loads(text), response.usage

    raise RuntimeError(f"Exhausted retries: {last_error}")
