"""GitLab HTTP API 最小客户端（M0-04）——仅使用 PAT + REST，不引入 python-gitlab SDK。"""

from __future__ import annotations

import uuid
from typing import Any

import httpx
from django.conf import settings


def _gitlab_headers() -> dict[str, str]:
    return {"PRIVATE-TOKEN": settings.TC_GITLAB_TOKEN}


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
            response = client.get(url, headers=_gitlab_headers())
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
            response = client.get(url, headers=_gitlab_headers())
            response.raise_for_status()
            data = response.json()
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "detail": str(exc)[:500]}
    return {"ok": True, "path_with_namespace": data.get("path_with_namespace")}


def gitlab_smoke_branch_commit_mr() -> dict[str, Any]:
    """在已配置项目中创建临时分支 → 单文件提交 → MR（W-A-03 阶段 B 演练）。"""
    base = settings.TC_GITLAB_URL
    token = settings.TC_GITLAB_TOKEN
    pid = settings.TC_GITLAB_PROJECT_ID
    if not base or not token or not pid:
        return {
            "ok": False,
            "step": "config",
            "detail": "需要 TC_GITLAB_URL、TC_GITLAB_TOKEN、TC_GITLAB_PROJECT_ID",
        }
    verify = settings.TC_GITLAB_SSL_VERIFY
    api = f"{base.rstrip('/')}/api/v4/projects/{pid}"
    branch = f"tc/wave-a-smoke-{uuid.uuid4().hex[:12]}"
    marker = uuid.uuid4().hex
    file_path = f"timberclaw-wave-a-smoke/{marker}.md"
    body_md = (
        f"TimberClaw Wave A GitLab smoke marker `{marker}`.\n\n"
        "Safe to delete this branch after review.\n"
    )

    try:
        with httpx.Client(timeout=30.0, verify=verify) as client:
            pr = client.get(api, headers=_gitlab_headers())
            pr.raise_for_status()
            project = pr.json()
            target = project.get("default_branch") or "main"

            commit_url = f"{api}/repository/commits"
            commit_payload = {
                "branch": branch,
                "start_branch": target,
                "commit_message": f"chore(timberclaw): wave-a gitlab smoke {marker[:8]}",
                "actions": [
                    {
                        "action": "create",
                        "file_path": file_path,
                        "content": body_md,
                    },
                ],
            }
            cr = client.post(
                commit_url,
                headers=_gitlab_headers(),
                json=commit_payload,
            )
            cr.raise_for_status()
            commit = cr.json()

            mr_url = f"{api}/merge_requests"
            mr_payload = {
                "source_branch": branch,
                "target_branch": target,
                "title": f"TimberClaw Wave A smoke ({marker[:8]})",
                "remove_source_branch": True,
            }
            mr = client.post(mr_url, headers=_gitlab_headers(), json=mr_payload)
            mr.raise_for_status()
            mr_data = mr.json()
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text[:800] if exc.response is not None else str(exc)
        return {"ok": False, "step": "http", "detail": detail, "status_code": exc.response.status_code if exc.response else None}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "step": "error", "detail": str(exc)[:800]}

    return {
        "ok": True,
        "target_branch": target,
        "source_branch": branch,
        "file_path": file_path,
        "commit_id": commit.get("id"),
        "commit_short_id": commit.get("short_id"),
        "merge_request": {
            "iid": mr_data.get("iid"),
            "web_url": mr_data.get("web_url"),
        },
    }
