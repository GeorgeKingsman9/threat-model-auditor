"""Small, explicit inference adapters; no automatic retries or hidden fallback."""

import hashlib
import json
import math
import os
import urllib.error
import urllib.request


class BudgetExceeded(ValueError):
    pass


class ModelClient:
    def __init__(self, provider, model, max_cost_usd, input_price, output_price,
                 max_output_tokens=4000, max_calls=28, allow_api=False):
        if not allow_api:
            raise ValueError("API inference requires --allow-api and an explicit spending limit")
        if provider not in {"openai", "anthropic"}:
            raise ValueError("provider must be openai or anthropic")
        if not model or any(not isinstance(value, (int, float)) or isinstance(value, bool)
                            or not math.isfinite(value) or value <= 0
                            for value in (max_cost_usd, input_price, output_price)):
            raise ValueError("model, positive budget, and positive per-million token prices are required")
        if any(type(value) is not int or value <= 0 for value in (max_calls, max_output_tokens)):
            raise ValueError("call and output limits must be positive")
        self.provider, self.model = provider, model
        self.limit, self.input_price, self.output_price = max_cost_usd, input_price, output_price
        self.max_output_tokens, self.max_calls = max_output_tokens, max_calls
        self.charged = 0.0
        self.calls = []

    def generate(self, system, content, schema):
        key_name = "OPENAI_API_KEY" if self.provider == "openai" else "ANTHROPIC_API_KEY"
        key = os.environ.get(key_name)
        if not key:
            raise ValueError(f"{key_name} is not configured")
        prompt = json.dumps(content, ensure_ascii=False)
        # UTF-8 bytes + schema + generous protocol overhead give a conservative
        # token reservation for the documented byte-based tokenizers. Prices are
        # operator-supplied; the ledger is a local guard, not a billing guarantee.
        input_bound = len((system + prompt + json.dumps(schema)).encode("utf-8")) + 4096
        reservation = (input_bound * self.input_price + self.max_output_tokens * self.output_price) / 1e6
        if len(self.calls) >= self.max_calls or self.charged + reservation > self.limit:
            raise BudgetExceeded("local inference budget/call limit reached; no request sent")
        if self.provider == "openai":
            url = "https://api.openai.com/v1/responses"
            payload = {
                "model": self.model, "store": False,
                "instructions": system, "input": prompt,
                "max_output_tokens": self.max_output_tokens,
                "text": {"format": {"type": "json_schema", "name": "audit", "strict": True, "schema": schema}},
            }
            headers = {"Authorization": "Bearer " + key}
        else:
            url = "https://api.anthropic.com/v1/messages"
            payload = {
                "model": self.model, "max_tokens": self.max_output_tokens,
                "system": system, "messages": [{"role": "user", "content": prompt}],
                "tools": [{"name": "emit_audit", "description": "Emit the requested audit record", "input_schema": schema}],
                "tool_choice": {"type": "tool", "name": "emit_audit"},
            }
            headers = {"x-api-key": key, "anthropic-version": "2023-06-01"}
        entry = {"provider": self.provider, "model": self.model,
                 "request_sha256": hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest(),
                 "reserved_usd": reservation, "status": "dispatched"}
        self.calls.append(entry)
        self.charged += reservation
        request = urllib.request.Request(
            url, data=json.dumps(payload).encode(),
            headers={**headers, "Content-Type": "application/json"}, method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                result = json.load(response)
        except urllib.error.HTTPError as error:
            # Do not echo provider bodies, auth headers or the request text.
            entry["status"] = "http_error"
            raise ValueError(f"{self.provider} API returned HTTP {error.code}; no retry") from None
        except (OSError, ValueError) as error:
            entry["status"] = "transport_or_response_error"
            raise ValueError("API request failed; reservation retained and no retry attempted") from None
        usage = result.get("usage", {})
        entry.update(status="received", usage=usage, response_id=result.get("id"))
        if all(type(usage.get(field)) is int and usage[field] >= 0
               for field in ("input_tokens", "output_tokens")):
            actual = (usage["input_tokens"] * self.input_price + usage["output_tokens"] * self.output_price) / 1e6
            entry["estimated_actual_usd"] = actual
            self.charged += actual - reservation
        else:
            entry["usage_invalid_reservation_retained"] = True
        if self.provider == "anthropic":
            if result.get("stop_reason") != "tool_use":
                raise ValueError("model output incomplete or refused; no verdict produced")
            outputs = [item["input"] for item in result.get("content", [])
                       if item.get("type") == "tool_use" and item.get("name") == "emit_audit"]
        else:
            if result.get("status") != "completed":
                raise ValueError("model output incomplete or refused; no verdict produced")
            outputs = [json.loads(part["text"]) for item in result.get("output", [])
                       for part in item.get("content", []) if part.get("type") == "output_text"]
        if len(outputs) != 1 or not isinstance(outputs[0], dict):
            raise ValueError("expected exactly one structured audit output")
        return outputs[0]

    def ledger(self):
        return {"provider": self.provider, "model": self.model,
                "limit_usd": self.limit, "charged_or_reserved_usd": round(self.charged, 6),
                "pricing_per_million": {"input": self.input_price, "output": self.output_price},
                "calls": self.calls}
