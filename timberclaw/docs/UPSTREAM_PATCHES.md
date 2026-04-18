# 上游相关修改登记（TimberClaw）

> 凡改动根目录 `docker-compose.yml`、根 `Makefile` 等 OpenHands 共享维护面时，在此登记，便于合并上游与复盘。

## 登记

| 日期 (UTC) | 文件 | 摘要 | Commit 标记 |
|------------|------|------|-------------|
| 2026-04-19 | `docker-compose.yml` | 增加 `postgres` 与 `tc-backend`（TimberClaw Django + PG），满足 PRD §6.1 / M0-01 | `[upstream-patch]` |
| 2026-04-19 | `Makefile` | 增加 `ensure-poetry-virtualenvs-path`，修复 Poetry 2 在最小环境下缺少 `virtualenvs.path` 目录导致 pre-commit 安装失败 | `[upstream-patch]` |
| 2026-04-19 | `frontend/.eslintrc` | 为 `src/timberclaw/**` 关闭 `i18next/no-literal-string`（中文占位 UI，术语映射层在 M4-06 统一） | `[upstream-patch]` |
| 2026-04-19 | `README.md`（根） | 目录树与 compose 说明对齐 M0-01 Batch 2 落地状态 | `[upstream-patch]` |
| 2026-04-19 | `timberclaw/backend/Dockerfile` | 复制 `pytest.ini` / `tests/` 以便 `docker compose run tc-backend python -m pytest` | `[upstream-patch]` |
| 2026-04-19 | `.gitignore`（根） | 取消忽略 `timberclaw/backend/requirements.txt`，使 Django 依赖清单可被版本控制 | `[upstream-patch]` |
| 2026-04-20 | `docker-compose.yml` | `tc-backend` 增加 LLM / GitLab 相关环境变量占位（与 M0-03 / M0-04 对齐） | `[upstream-patch]` |
