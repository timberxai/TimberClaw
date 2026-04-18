"""统一 LLM 出口（M0-03）。厂商通过环境变量切换，不在代码里硬编码 SDK。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx
from django.conf import settings


@dataclass
class ChatResult:
    text: str
    prompt_tokens: int
    completion_tokens: int


def _post_chat_completions(
    base_url: str,
    api_key: str,
    model: str,
    messages: list[dict[str, Any]],
    max_tokens: int,
    timeout: float,
) -> ChatResult:
    url = f"{base_url.rstrip('/')}/chat/completions"
    payload = {"model": model, "messages": messages, "max_tokens": max_tokens}
    headers = {"Authorization": f"Bearer {api_key}"}
    with httpx.Client(timeout=timeout) as client:
        response = client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
    choice = data["choices"][0]["message"]["content"]
    usage = data.get("usage") or {}
    return ChatResult(
        text=str(choice),
        prompt_tokens=int(usage.get("prompt_tokens") or 0),
        completion_tokens=int(usage.get("completion_tokens") or 0),
    )


def invoke_chat(
    messages: list[dict[str, Any]],
    *,
    max_output_tokens: int | None = None,
) -> ChatResult:
    """执行一次聊天补全；失败抛异常，由视图层写审计日志。"""
    provider = settings.TC_LLM_PROVIDER
    cap = settings.TC_LLM_MAX_OUTPUT_TOKENS
    max_out = min(max_output_tokens or cap, cap)
    timeout = float(settings.TC_LLM_TIMEOUT_SECONDS)

    if provider == "mock":
        last = messages[-1] if messages else {}
        content = last.get("content", "")
        return ChatResult(text=f"[mock] {content}", prompt_tokens=1, completion_tokens=1)

    if provider == "openai":
        if not settings.TC_OPENAI_API_KEY:
            raise ValueError("TC_OPENAI_API_KEY 未配置")
        return _post_chat_completions(
            settings.TC_OPENAI_BASE_URL,
            settings.TC_OPENAI_API_KEY,
            settings.TC_LLM_MODEL_OPENAI,
            messages,
            max_out,
            timeout,
        )

    if provider in ("dashscope", "qwen"):
        if not settings.TC_DASHSCOPE_API_KEY:
            raise ValueError("TC_DASHSCOPE_API_KEY 未配置")
        return _post_chat_completions(
            settings.TC_DASHSCOPE_BASE_URL,
            settings.TC_DASHSCOPE_API_KEY,
            settings.TC_LLM_MODEL_DASHSCOPE,
            messages,
            max_out,
            timeout,
        )

    raise ValueError(f"未知的 TC_LLM_PROVIDER: {provider}")


