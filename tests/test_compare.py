import unittest

from prompt_tester.compare import PromptResult, run_suite


class FakeClient:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def chat(self, system_prompt, user_prompt):
        self.calls.append((system_prompt, user_prompt))
        return self.responses[system_prompt]


class TestRunSuite(unittest.TestCase):
    def test_results_match_prompts(self):
        client = FakeClient({"sys-a": "resp-a", "sys-b": "resp-b"})
        results = run_suite(client, {"A": "sys-a", "B": "sys-b"}, "user text")
        self.assertEqual([r.name for r in results], ["A", "B"])
        self.assertTrue(all(r.ok for r in results))
        self.assertEqual(results[0].response, "resp-a")
        self.assertEqual(results[1].response, "resp-b")
        self.assertEqual(client.calls[0], ("sys-a", "user text"))
        self.assertEqual(client.calls[1], ("sys-b", "user text"))

    def test_error_recorded(self):
        class BadClient:
            def chat(self, system_prompt, user_prompt):
                raise RuntimeError("boom")

        results = run_suite(BadClient(), {"X": "sys"}, "user text")
        self.assertEqual(len(results), 1)
        self.assertFalse(results[0].ok)
        self.assertIn("boom", results[0].error)

    def test_result_ok_property(self):
        self.assertTrue(PromptResult("a", "s", "r").ok)
        self.assertFalse(PromptResult("a", "s", None, "err").ok)


if __name__ == "__main__":
    unittest.main()
