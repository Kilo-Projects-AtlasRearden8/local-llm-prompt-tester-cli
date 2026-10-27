import unittest

from prompt_tester.compare import PromptResult
from prompt_tester.report import build_report


class TestBuildReport(unittest.TestCase):
    def test_report_contains_results(self):
        results = [
            PromptResult("Creative", "Be creative.", "A story."),
            PromptResult("Strict", "Be strict.", None, "connection failed"),
        ]
        report = build_report(results, "Hello", "http://localhost:11434/v1/chat/completions", "llama3")
        self.assertIn("# Prompt Test Results", report)
        self.assertIn("Creative", report)
        self.assertIn("Strict", report)
        self.assertIn("A story.", report)
        self.assertIn("connection failed", report)
        self.assertIn("Hello", report)
        self.assertIn("llama3", report)

    def test_side_by_side_table(self):
        results = [PromptResult("One", "sys1", "resp1"), PromptResult("Two", "sys2", "resp2")]
        report = build_report(results, "hi", "http://x", "m")
        self.assertIn("| One | resp1 |", report)
        self.assertIn("| Two | resp2 |", report)


if __name__ == "__main__":
    unittest.main()
