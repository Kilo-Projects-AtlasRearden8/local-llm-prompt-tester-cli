# STATUS

## What was built

A local-first Python CLI for testing system prompts against a local LLM endpoint,
defaulting to Ollama (`http://localhost:11434/v1/chat/completions`) but
configurable to any OpenAI-compatible URL. It sends one user prompt to multiple
system prompts, shows the responses side by side in Markdown, and saves the
report to a file (or prints it to the terminal).

Built stdlib-only (no `requests`, `openai`, or API keys required), with a
test suite that runs entirely against a mock endpoint.

Files:
- `prompt_tester/cli.py` — argument parsing and entry point
- `prompt_tester/client.py` — OpenAI-compatible chat client over `urllib`
- `prompt_tester/compare.py` — runs one user prompt across many system prompts
- `prompt_tester/report.py` — Markdown report generation
- `tests/` — unittest suite with mock endpoint (mock_server.py)
- `README.md` — usage guide, credits Asdale Dynamics, LLC
- `LICENSE` — MIT, Copyright (c) 2026 Asdale Dynamics, LLC
- `pyproject.toml` — optional `pip install .` with `prompt-tester` entry point

## How to run

```bash
# See options
python3 -m prompt_tester.cli --help

# Compare two system prompts against a local Ollama instance
python3 -m prompt_tester.cli \
  -s "You are a friendly writing coach." -n Coach \
  -s "You are a grumpy editor." -n Editor \
  -u "Explain what a large language model is." \
  -o prompt_test_results.md

# Read prompts from files
python3 -m prompt_tester.cli \
  -S system_prompts/coach.txt -S system_prompts/editor.txt \
  -n Coach -n Editor \
  -U user_prompts/article.txt \
  -o results.md

# Custom endpoint / model
python3 -m prompt_tester.cli -s @sys.txt -u @user.txt \
  --url http://localhost:11434/v1/chat/completions --model llama3 --timeout 60
```

## Verification results

- `python3 -m unittest discover -s tests`: 12 tests, OK, exit code 0
- Tests cover: client request/response, connection failure, suite execution,
  error recording, report contents (side-by-side table + detailed sections),
  CLI stdout/file output, missing-argument errors, non-zero exit on failed requests
- End-to-end CLI run against live mock server: correct Markdown report, exit 0
- End-to-end CLI run against unreachable endpoint: graceful ERROR entry, exit 1
- `python3 -m py_compile prompt_tester/*.py tests/*.py`: compiles cleanly
- Python 3.13.5, stdlib-only, no dependencies to install

## Known gaps

- No streaming responses; waits for the full completion
- Default model `llama3` must exist in your Ollama (change with `--model`)
- Mock endpoint returns a fixed canned response; it does not echo the actual
  prompts (sufficient for CLI/report testing, not for response-quality testing)
- No config file or environment variable support yet; all options are CLI flags
- Side-by-side table escapes responses into single-line cells; full responses
  are in the Detailed Results section below
- No authentication support (intentionally none — local-first, no keys)
