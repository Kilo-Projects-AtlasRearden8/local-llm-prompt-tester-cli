import json
import urllib.error
import urllib.request


class LLMError(Exception):
    pass


class LLMClient:
    def __init__(self, url, model, timeout=60):
        self.url = url
        self.model = model
        self.timeout = timeout

    def chat(self, system_prompt, user_prompt):
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise LLMError(f"HTTP {exc.code}: {body}") from exc
        except urllib.error.URLError as exc:
            raise LLMError(f"Cannot reach {self.url}: {exc}") from exc
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError as exc:
            raise LLMError(f"Invalid JSON from endpoint: {body[:200]}") from exc
        try:
            return parsed["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMError(f"Unexpected response format: {body[:200]}") from exc
