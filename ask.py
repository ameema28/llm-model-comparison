"""ask.py — ask a question from the terminal.

Usage:
    python ask.py "What is a token?"
    python ask.py "What is a token?" --provider groq
"""
import argparse
import datetime
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, APITimeoutError, APIConnectionError

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

PROVIDERS = {
    "gemini": (os.getenv("GEMINI_API_KEY"), GEMINI_BASE_URL,
               os.getenv("GEMINI_MODEL", "gemini-3.8-flash")),
    "groq": (os.getenv("GROQ_API_KEY"), GROQ_BASE_URL,
             os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")),
}

SYSTEM_PROMPT = (
    "You are a concise study assistant for computer science students. "
    "Answer in plain English in at most 4 sentences. "
    "If you are not sure of an answer, say 'I don't know' instead of guessing. "
    "Never ask the user to repeat the question."
)

RETRYABLE = (RateLimitError, APITimeoutError, APIConnectionError)
LOG_FILE = BASE_DIR / "logs" / "calls.jsonl"


def ask(client, model, question, retries=3, timeout=30):
    """Send the question; retry transient errors with back-off (2s, 4s, 8s)."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    for attempt in range(1, retries + 1):
        try:
            return client.chat.completions.create(
                model=model, messages=messages, timeout=timeout
            )
        except RETRYABLE as e:
            wait = 2 ** attempt
            print(f"Retry {attempt} in {wait}s: {type(e).__name__}", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError("All retries failed")


def log_call(provider, model, usage, latency, ok=True, error=None):
    """Append one JSON line per call. Never log API keys or personal data."""
    LOG_FILE.parent.mkdir(exist_ok=True)
    record = {
        "time": datetime.datetime.now().isoformat(timespec="seconds"),
        "provider": provider,
        "model": model,
        "tokens_in": usage.prompt_tokens if usage else None,
        "tokens_out": usage.completion_tokens if usage else None,
        "latency_s": round(latency, 2),
        "ok": ok,
        "error": error,
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Ask a question to an LLM.")
    parser.add_argument("question")
    parser.add_argument("--provider", choices=["gemini", "groq"], default="gemini")
    args = parser.parse_args()

    key, base_url, model = PROVIDERS[args.provider]
    if not key:
        sys.exit(f"Missing API key for '{args.provider}'. Check your .env file.")

    client = OpenAI(api_key=key, base_url=base_url, max_retries=0)

    start = time.perf_counter()
    try:
        r = ask(client, model, args.question)
    except Exception as e:
        log_call(args.provider, model, None, time.perf_counter() - start,
                 ok=False, error=type(e).__name__)
        sys.exit(f"Failed: {type(e).__name__}: {e}")

    latency = time.perf_counter() - start
    log_call(args.provider, model, r.usage, latency)

    print(r.choices[0].message.content)
    print("-" * 40)
    if r.usage:
        print("tokens in: ", r.usage.prompt_tokens)
        print("tokens out:", r.usage.completion_tokens)
    print(f"latency:    {latency:.2f}s")


if __name__ == "__main__":
    main()
