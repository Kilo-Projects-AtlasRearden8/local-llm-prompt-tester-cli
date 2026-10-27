import argparse
import sys

from .client import LLMClient, LLMError
from .compare import run_suite
from .report import build_report

DEFAULT_URL = "http://localhost:11434/v1/chat/completions"
DEFAULT_MODEL = "llama3"


def load_text(value):
    if value.startswith("@"):
        with open(value[1:], "r", encoding="utf-8") as fh:
            return fh.read()
    return value


def build_parser():
    parser = argparse.ArgumentParser(
        description="Test system prompts against a local LLM endpoint (default Ollama)."
    )
    parser.add_argument("-s", "--system-prompt", action="append", default=[],
                        help="System prompt text, or @path to a file. Repeatable.")
    parser.add_argument("-S", "--system-prompt-file", action="append", default=[],
                        help="Path to a file containing a system prompt. Repeatable.")
    parser.add_argument("-n", "--name", action="append", default=[],
                        help="Name for a system prompt, in order of -s/-S. Repeatable.")
    parser.add_argument("-u", "--user-prompt", help="User prompt text, or @path to a file.")
    parser.add_argument("-U", "--user-prompt-file", help="Path to a file containing the user prompt.")
    parser.add_argument("--url", default=DEFAULT_URL, help="OpenAI-compatible chat completions URL.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model name.")
    parser.add_argument("--timeout", type=int, default=60, help="Request timeout in seconds.")
    parser.add_argument("-o", "--output", help="Write Markdown report to this file.")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    system_inputs = list(args.system_prompt) + list(args.system_prompt_file)
    if not system_inputs:
        parser.error("at least one system prompt is required (-s or -S)")
    if not args.user_prompt and not args.user_prompt_file:
        parser.error("a user prompt is required (-u or -U)")

    if args.user_prompt:
        try:
            user_prompt = load_text(args.user_prompt)
        except OSError as exc:
            print(f"error: cannot read user prompt: {exc}", file=sys.stderr)
            return 1
    else:
        try:
            user_prompt = load_text("@" + args.user_prompt_file)
        except OSError as exc:
            print(f"error: cannot read user prompt: {exc}", file=sys.stderr)
            return 1

    prompts = {}
    for index, item in enumerate(system_inputs):
        try:
            text = load_text(item)
        except OSError as exc:
            print(f"error: cannot read system prompt {item}: {exc}", file=sys.stderr)
            return 1
        if index < len(args.name):
            name = args.name[index]
        else:
            name = item if len(system_inputs) == 1 else f"Prompt {index + 1}"
        prompts[name] = text

    client = LLMClient(args.url, args.model, args.timeout)
    results = run_suite(client, prompts, user_prompt)
    report = build_report(results, user_prompt, args.url, args.model)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as fh:
                fh.write(report)
        except OSError as exc:
            print(f"error: cannot write output: {exc}", file=sys.stderr)
            return 1
    else:
        sys.stdout.write(report)
        sys.stdout.write("\n")

    failed = [r for r in results if not r.ok]
    if failed:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
