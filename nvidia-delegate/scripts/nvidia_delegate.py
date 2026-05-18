#!/usr/bin/env python3
"""Call NVIDIA NIM / API Catalog OpenAI-compatible chat models."""

from __future__ import annotations

import argparse
import json
import os
import re
import socket
import sys
import urllib.error
import urllib.request
from typing import Any


DEFAULT_BASE_URL = "https://integrate.api.nvidia.com/v1"

MODEL_ALIASES = {
    "llama-small": "meta/llama-3.1-8b-instruct",
    "glm": "z-ai/glm-5.1",
    "zai-glm": "z-ai/glm-5.1",
    "deepseek-flash": "deepseek-ai/deepseek-v4-flash",
    "deepseek-pro": "deepseek-ai/deepseek-v4-pro",
    "deepseek-coder": "deepseek-ai/deepseek-coder-6.7b-instruct",
    "qwen-coder": "qwen/qwen3-coder-480b-a35b-instruct",
    "qwen-large": "qwen/qwen3.5-397b-a17b",
}


def api_key() -> str:
    key = os.environ.get("NVIDIA_API_KEY") or os.environ.get("NGC_API_KEY")
    if not key:
        raise SystemExit("NVIDIA_API_KEY or NGC_API_KEY is not set.")
    return key


def normalize_model(model: str) -> str:
    return MODEL_ALIASES.get(model.strip(), model.strip())


def read_prompt(args: argparse.Namespace) -> str:
    chunks: list[str] = []
    if args.prompt:
        chunks.append(args.prompt)
    if args.prompt_file:
        with open(args.prompt_file, "r", encoding="utf-8") as f:
            chunks.append(f.read())
    if not sys.stdin.isatty():
        data = sys.stdin.read()
        if data.strip():
            chunks.append(data)
    prompt = "\n\n".join(chunk.strip() for chunk in chunks if chunk.strip())
    if not prompt and not args.list_models:
        raise SystemExit("Provide --prompt, --prompt-file, or stdin.")
    return prompt


def request_json(base_url: str, path: str, payload: dict[str, Any] | None, timeout: int) -> dict[str, Any]:
    url = base_url.rstrip("/") + path
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key()}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="GET" if payload is None else "POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {exc.code} from NVIDIA API: {body[:1000]}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Could not reach NVIDIA API: {exc}") from exc
    except (TimeoutError, socket.timeout) as exc:
        raise SystemExit(
            f"NVIDIA API request timed out after {timeout}s. Try --timeout 120 or another model alias."
        ) from exc


def list_models(args: argparse.Namespace) -> int:
    data = request_json(args.base_url, "/models", None, args.timeout)
    models = sorted({item.get("id", "") for item in data.get("data", []) if item.get("id")})
    if args.filter:
        pattern = re.compile(args.filter, re.IGNORECASE)
        models = [model for model in models if pattern.search(model)]
    for model in models:
        print(model)
    return 0


def chat_once(model: str, prompt: str, args: argparse.Namespace) -> str:
    messages = []
    if args.system:
        messages.append({"role": "system", "content": args.system})
    messages.append({"role": "user", "content": prompt})
    payload: dict[str, Any] = {
        "model": normalize_model(model),
        "messages": messages,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "stream": False,
    }
    if args.json_output:
        payload["response_format"] = {"type": "json_object"}

    data = request_json(args.base_url, "/chat/completions", payload, args.timeout)
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise SystemExit(f"Unexpected NVIDIA API response: {json.dumps(data)[:1000]}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Delegate a prompt to NVIDIA-hosted chat models.")
    parser.add_argument("--base-url", default=os.environ.get("NVIDIA_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--model", default="llama-small", help="Alias or full model ID. Default: llama-small")
    parser.add_argument("--compare", help="Comma-separated aliases/model IDs to run against the same prompt.")
    parser.add_argument("--system", default="Be concise, accurate, and explicit about uncertainty.")
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int, default=1200)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--json-output", action="store_true", help="Request JSON object output from compatible models.")
    parser.add_argument("--list-models", action="store_true")
    parser.add_argument("--filter", help="Regex filter for --list-models.")
    args = parser.parse_args()

    if args.list_models:
        return list_models(args)

    prompt = read_prompt(args)
    models = [m.strip() for m in args.compare.split(",")] if args.compare else [args.model]
    models = [m for m in models if m]

    for index, model in enumerate(models):
        if len(models) > 1:
            if index:
                print()
            print(f"## {model} ({normalize_model(model)})")
        print(chat_once(model, prompt, args).strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
