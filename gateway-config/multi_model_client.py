#!/usr/bin/env python3
"""Multi-model inference client via 9Router (OpenAI-compatible).

Setup:
    export GATEWAY_URL="http://localhost:20128/v1"
    export GATEWAY_KEY="your-gateway-key"

Usage:
    from multi_model_client import chat
    answer = chat("Explain quantum entanglement in 2 sentences.")
    answer = chat("Refactor this code", model="deepseek-v4-flash")
    answer = chat(prompt, models=["claude-sonnet-4", "deepseek-v4-flash", "qwen2.5-coder-32b"])
"""
import httpx
import os
from typing import Optional

GATEWAY_URL = os.environ["GATEWAY_URL"]
GATEWAY_KEY = os.environ["GATEWAY_KEY"]

DEFAULT_MODEL = "Combo-Agent"


def chat(
    prompt: str,
    model: str = DEFAULT_MODEL,
    models: Optional[list] = None,
    system: Optional[str] = None,
    max_tokens: int = 2000,
    temperature: float = 0.7,
    timeout: int = 60,
) -> str:
    """Send a chat completion request. Supports automatic fallback chain."""
    candidates = models or [model]
    last_err = None

    for m in candidates:
        try:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            r = httpx.post(
                f"{GATEWAY_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {GATEWAY_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": m,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                },
                timeout=timeout,
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            last_err = (m, str(e))
            continue

    raise RuntimeError(f"All models failed. Last: {last_err}")


def stream_chat(prompt: str, model: str = DEFAULT_MODEL, **kwargs):
    """Streaming variant. Yields text chunks."""
    with httpx.stream(
        "POST",
        f"{GATEWAY_URL}/chat/completions",
        headers={"Authorization": f"Bearer {GATEWAY_KEY}"},
        json={"model": model, "messages": [{"role": "user", "content": prompt}], "stream": True, **kwargs},
        timeout=60,
    ) as r:
        for line in r.iter_lines():
            if line.startswith("data: "):
                payload = line[6:]
                if payload == "[DONE]":
                    break
                import json
                try:
                    chunk = json.loads(payload)
                    delta = chunk["choices"][0]["delta"].get("content")
                    if delta:
                        yield delta
                except Exception:
                    continue


if __name__ == "__main__":
    print(chat("Hello, what's 2+2?"))
