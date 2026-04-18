"""GitLab HTTP API 最小客户端（M0-04）——仅使用 PAT + REST，不引入 python-gitlab SDK。"""

from __future__ import annotations

from typing import Any

import httpx
from django.conf import settings


def gitlab_version_payload() -> dict[str, Any]:
    """调用 GET /api/v4/version；未配置 URL/Token 时返回 skipped。"""
    base = settings.TC_GITLAB_URL
    token = settings.TC_GITLAB_TOKEN
    if not base or not token:
        return {
            "ok": False,
            "skipped": True,
            "detail": "TC_GITLAB_URL 或 TC_GITLAB_TOKEN 未配置",
        }
    url = f"{base.rstrip('/')}/api/v4/version"
    verify = settings.TC_GITLAB_SSL_VERIFY
    try:
        with httpx.Client(timeout=10.0, verify=verify) as client:
            response = client.get(url, headers={"PRIVATE-TOKEN": token})
            response.raise_for_status()
            data = response.json()
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "skipped": False, "detail": str(exc)[:500]}
    return {
        "ok": True,
        "skipped": False,
        "version": data.get("version"),
        "revision": data.get("revision"),
    }


def gitlab_project_probe() -> dict[str, Any] | None:
    """若配置了 TC_GITLAB_PROJECT_ID，则探测项目可读性。"""
    pid = settings.TC_GITLAB_PROJECT_ID
    base = settings.TC_GITLAB_URL
    token = settings.TC_GITLAB_TOKEN
    if not pid or not base or not token:
        return None
    url = f"{base.rstrip('/')}/api/v4/projects/{pid}"
    verify = settings.TC_GITLAB_SSL_VERIFY
    try:
        with httpx.Client(timeout=10.0, verify=verify) as client:
            response = client.get(url, headers={"PRIVATE-TOKEN": token})
            response.raise_for_status()
            data = response.json()
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "detail": str(exc)[:500]}
    return {"ok": True, "path_with_namespace": data.get("path_with_namespace")}
