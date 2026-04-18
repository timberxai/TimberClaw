#!/usr/bin/env bash
# Wave A 统一自检（M0-05 / W-A-04）：Postgres 宿主机端口 + Django 健康链（/api/health/ 含 DB SELECT 1）+ 可选 pytest / pre-commit
#
# 用法（仓库根目录，且 tc-backend 已对宿主暴露 8000）：
#   bash scripts/tc_wave_a_check.sh
#
# 环境变量：
#   TC_BACKEND_URL          默认 http://127.0.0.1:8000
#   TC_POSTGRES_HOST        默认 127.0.0.1
#   TC_POSTGRES_PORT        默认 5433（与 docker-compose 中 TC_POSTGRES_PORT 对齐）
#   TC_WAVE_A_SKIP_POSTGRES 设为 1 则跳过 TCP 探测（例如仅跑 API 的 CI 片段）
#   TC_WAVE_A_RUN_PYTEST    设为 1 则执行 docker compose run --rm tc-backend python -m pytest
#   TC_WAVE_A_RUN_PRE_COMMIT 设为 1 则执行 pre-commit run --all-files（需本机已安装 pre-commit）
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

TC_BACKEND="${TC_BACKEND_URL:-http://127.0.0.1:8000}"
PG_HOST="${TC_POSTGRES_HOST:-127.0.0.1}"
PG_PORT="${TC_POSTGRES_PORT:-5433}"

postgres_tcp_ok() {
  if [[ "${TC_WAVE_A_SKIP_POSTGRES:-0}" == "1" ]]; then
    echo "==> Postgres TCP: skipped (TC_WAVE_A_SKIP_POSTGRES=1)"
    return 0
  fi
  echo "==> Postgres TCP ${PG_HOST}:${PG_PORT}"
  if command -v nc >/dev/null 2>&1 && nc -z -w 2 "$PG_HOST" "$PG_PORT" 2>/dev/null; then
    echo "OK: postgres port reachable (nc)"
    return 0
  fi
  if command -v bash >/dev/null 2>&1 && bash -c "exec 3<>/dev/tcp/${PG_HOST}/${PG_PORT}" 2>/dev/null; then
    echo "OK: postgres port reachable (bash /dev/tcp)"
    return 0
  fi
  if ! command -v nc >/dev/null 2>&1 && ! command -v bash >/dev/null 2>&1; then
    echo "WARN: no nc or bash; skipping postgres TCP probe"
    return 0
  fi
  echo "FAIL: cannot reach postgres at ${PG_HOST}:${PG_PORT} (is compose up?)"
  return 1
}

curl_json() {
  local url=$1
  echo "==> GET ${url}"
  if command -v jq >/dev/null 2>&1; then
    curl -fsS "$url" | jq .
  else
    curl -fsS "$url"
    echo
  fi
}

postgres_tcp_ok

echo "==> Django root health (via scripts/tc_compose_health.sh)"
bash "${ROOT}/scripts/tc_compose_health.sh"

for path in /api/health/llm/ /api/health/gitlab/; do
  curl_json "${TC_BACKEND}${path}"
  echo
done

if [[ "${TC_WAVE_A_RUN_PYTEST:-0}" == "1" ]]; then
  echo "==> pytest (docker compose run --rm tc-backend)"
  docker compose run --rm tc-backend python -m pytest
fi

if [[ "${TC_WAVE_A_RUN_PRE_COMMIT:-0}" == "1" ]]; then
  echo "==> pre-commit run --all-files"
  if command -v pre-commit >/dev/null 2>&1; then
    pre-commit run --all-files
  else
    echo "FAIL: pre-commit not on PATH (install hooks per W-A-00 / Makefile)"
    exit 1
  fi
fi

echo "OK: wave-a check (api trio + postgres tcp; pytest/pre-commit if enabled)"
