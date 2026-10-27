import unittest

from prompt_tester.client import LLMClient, LLMError
from tests.mock_server import start


class TestLLMClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server, cls.port = start()
        cls.url = f"http://127.0.0.1:{cls.port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def test_chat_returns_content(self):
        client = LLMClient(self.url, "test-model")
        response = client.chat("You are helpful.", "Say hello.")
        self.assertEqual(response, "Mock response from the local endpoint.")

    def test_connection_refused(self):
        client = LLMClient("http://127.0.0.1:1", "test-model", timeout=2)
        with self.assertRaises(LLMError):
            client.chat("sys", "user")


if __name__ == "__main__":
    unittest.main()
