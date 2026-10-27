from .client import LLMClient


class PromptResult:
    def __init__(self, name, system_prompt, response, error=None):
        self.name = name
        self.system_prompt = system_prompt
        self.response = response
        self.error = error

    @property
    def ok(self):
        return self.error is None


def run_suite(client, prompts, user_prompt):
    results = []
    for name, system_prompt in prompts.items():
        try:
            response = client.chat(system_prompt, user_prompt)
            results.append(PromptResult(name, system_prompt, response))
        except Exception as exc:
            results.append(PromptResult(name, system_prompt, None, str(exc)))
    return results
