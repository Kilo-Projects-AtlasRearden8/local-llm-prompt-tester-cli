# Prompt Tester CLI

A small, local-first Python CLI for testing system prompts against a local LLM
endpoint (Ollama by default, or any OpenAI-compatible URL). Run several system
prompts side by side, compare the outputs, and save the results as Markdown.

Built by **Asdale Dynamics, LLC** — beginner-friendly AI education, books, and
practical tools. Plain English, step by step, never condescending.

## What it does

- Sends a system prompt and a user prompt to your local LLM endpoint
- Tests multiple system prompts at once and shows their responses side by side
- Writes a Markdown report you can read, share, or publish
- Works with Ollama out of the box (default: `http://localhost:11434/v1/chat/completions`)
- Needs no API keys — it talks to a local endpoint you control

## Install

No installation is required. Just run it with Python 3.8+:

```bash
python3 -m prompt_tester.cli --help
```

If you want it on your PATH:

```bash
pip install .
prompt-tester --help
```

## Quick start

Make sure your local LLM is running (for example, Ollama on port 11434), then:

```bash
python3 -m prompt_tester.cli \
  -s "You are a friendly writing coach." \
  -n "Coach" \
  -s "You are a grumpy editor." \
  -n "Editor" \
  -u "Explain what a large language model is." \
  -o prompt_test_results.md
```

This sends the same user prompt to two different system prompts, compares the
answers side by side, and saves `prompt_test_results.md`.

### Reading from files

Long prompts are easier to keep in files. Use `@path` to read a prompt from a
file:

```bash
python3 -m prompt_tester.cli \
  -s @system_prompts/coach.txt \
  -s @system_prompts/editor.txt \
  -u @user_prompts/article.txt \
  -o results.md
```

Or use the file-specific flags:

```bash
python3 -m prompt_tester.cli \
  -S system_prompts/coach.txt \
  -S system_prompts/editor.txt \
  -U user_prompts/article.txt \
  -n Coach \
  -n Editor \
  -o results.md
```

### Options

| Option | Meaning |
|--------|---------|
| `-s`, `--system-prompt` | System prompt text, or `@path` to a file. Repeatable. |
| `-S`, `--system-prompt-file` | File containing a system prompt. Repeatable. |
| `-n`, `--name` | Name for each system prompt, in order. Repeatable. |
| `-u`, `--user-prompt` | User prompt text, or `@path` to a file. |
| `-U`, `--user-prompt-file` | File containing the user prompt. |
| `--url` | OpenAI-compatible chat completions URL (default Ollama). |
| `--model` | Model name (default `llama3`). |
| `--timeout` | Request timeout in seconds (default 60). |
| `-o`, `--output` | Write the Markdown report to this file (default: print to terminal). |

## Example report

The Markdown report includes:

- The endpoint, model, and timestamp
- Your user prompt
- A side-by-side comparison table of every system prompt's response
- A detailed section per prompt with the full system prompt and full response

## Tests

Run the test suite (uses a mock endpoint, no network or keys needed):

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.

## About

Asdale Dynamics, LLC (Indiana, formed October 2026) is founded by Dylan Asdale,
a registered nurse turned AI author. He writes AI explainers "like a friend
would" — plain English, step by step, never condescending — at
dylanasdale.github.io and in his book _The Massive AI Manual_. This tool is part
of the LLC's open-source collection of local-LLM utilities and beginner-friendly
AI resources.
