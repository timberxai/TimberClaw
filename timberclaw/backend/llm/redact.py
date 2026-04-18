"""出站前敏感信息脱敏（PRD §8.5）——最小规则集，后续与 M3 审计联动扩展。"""

from __future__ import annotations

import re

_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"(?i)(api[_-]?key|password|token|secret)\s*[:=]\s*\S+"), r"\1=***"),
    (re.compile(r"(?i)Bearer\s+[A-Za-z0-9\-._~+/]+=*"), "Bearer ***"),
    (re.compile(r"(?i)(Authorization)\s*:\s*\S+"), r"\1: ***"),
    (re.compile(r"\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"), "10.*.*.*"),
    (re.compile(r"\b192\.168\.\d{1,3}\.\d{1,3}\b"), "192.168.*.*"),
)


def redact_text(text: str) -> str:
    out = text
    for pattern, repl in _PATTERNS:
        out = pattern.sub(repl, out)
    return out


def redact_messages(messages: list[dict]) -> list[dict]:
    """返回脱敏后的消息副本，不修改入参。"""
    cleaned: list[dict] = []
    for m in messages:
        mm = dict(m)
        if isinstance(mm.get("content"), str):
            mm["content"] = redact_text(mm["content"])
        cleaned.append(mm)
    return cleaned
