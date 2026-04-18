#!/usr/bin/env bash
# Quick smoke: Django GET /api/health/ only（完整 Wave A 自检见 scripts/tc_wave_a_check.sh）。
set -euo pipefail

TC_BACKEND="${TC_BACKEND_URL:-http://127.0.0.1:8000}"

echo "==> GET ${TC_BACKEND}/api/health/"
if command -v jq >/dev/null 2>&1; then
  curl -fsS "${TC_BACKEND}/api/health/" | jq .
else
  curl -fsS "${TC_BACKEND}/api/health/"
  echo
fi

echo "OK: tc-backend health"
