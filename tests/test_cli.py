import io
import sys
import tempfile
import unittest
from unittest import mock

from prompt_tester import cli


class FakeClient:
    def __init__(self, response="ok"):
        self.response = response
        self.calls = []

    def chat(self, system_prompt, user_prompt):
        self.calls.append((system_prompt, user_prompt))
        return self.response


class TestCLI(unittest.TestCase):
    def test_missing_system_prompt_errors(self):
        with mock.patch.object(sys, "argv", ["prog", "-u", "hi"]):
            with self.assertRaises(SystemExit) as ctx:
                cli.main()
        self.assertEqual(ctx.exception.code, 2)

    def test_missing_user_prompt_errors(self):
        with mock.patch.object(sys, "argv", ["prog", "-s", "sys"]):
            with self.assertRaises(SystemExit) as ctx:
                cli.main()
        self.assertEqual(ctx.exception.code, 2)

    def test_writes_markdown_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = f"{tmp}/result.md"
            with mock.patch.object(sys, "argv", ["prog",
                                                  "-s", "You are a poet.",
                                                  "-n", "Poet",
                                                  "-u", "Write a line.",
                                                  "--url", "http://127.0.0.1:9",
                                                  "--output", out]):
                with mock.patch("prompt_tester.cli.LLMClient", return_value=FakeClient()):
                    code = cli.main()
            self.assertEqual(code, 0)
            with open(out, encoding="utf-8") as fh:
                content = fh.read()
            self.assertIn("# Prompt Test Results", content)
            self.assertIn("Poet", content)
            self.assertIn("Write a line.", content)
            self.assertIn("ok", content)

    def test_prints_to_stdout(self):
        with mock.patch.object(sys, "argv", ["prog",
                                              "-s", "sys text",
                                              "-u", "user text",
                                              "--url", "http://127.0.0.1:9"]):
            with mock.patch("prompt_tester.cli.LLMClient", return_value=FakeClient("resp")):
                with mock.patch.object(sys, "stdout", io.StringIO()) as out:
                    code = cli.main()
        self.assertEqual(code, 0)
        self.assertIn("resp", out.getvalue())
        self.assertIn("user text", out.getvalue())

    def test_failed_request_returns_nonzero(self):
        class FailingClient:
            def chat(self, system_prompt, user_prompt):
                from prompt_tester.client import LLMError
                raise LLMError("down")

        with mock.patch.object(sys, "argv", ["prog",
                                              "-s", "sys",
                                              "-u", "user",
                                              "--url", "http://127.0.0.1:9"]):
            with mock.patch("prompt_tester.cli.LLMClient", return_value=FailingClient()):
                code = cli.main()
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
