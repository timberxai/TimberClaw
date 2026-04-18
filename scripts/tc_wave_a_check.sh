#!/usr/bin/env bash
# Wave A 自检：Django 根健康 + LLM 配置探测 + GitLab 连通（M0-05 草案）
set -euo pipefail

TC_BACKEND="${TC_BACKEND_URL:-http://127.0.0.1:8000}"

for path in /api/health/ /api/health/llm/ /api/health/gitlab/; do
  echo "==> GET ${TC_BACKEND}${path}"
  curl -fsS "${TC_BACKEND}${path}" | (command -v jq >/dev/null 2>&1 && jq . || cat)
  echo
done

echo "OK: wave-a health trio"
