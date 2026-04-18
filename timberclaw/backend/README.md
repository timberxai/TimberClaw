# TimberClaw Builder API（Django）

独立 Django 服务，与 OpenHands 的 FastAPI/Python 依赖栈分离，便于按 PRD §6.1 演进工厂业务 API 与后续生成系统元数据。

## 本地（无 Docker）

```bash
cd timberclaw/backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DJANGO_DEBUG=1
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

健康检查：`GET /api/health/`（含 `checks.database`：`SELECT 1`；失败时 HTTP **503**）

## LLM Gateway（M0-03）

- `GET /api/health/llm/` — 当前 `TC_LLM_PROVIDER` 与密钥是否就绪（默认 `mock` 无需密钥）
- `POST /api/llm/invoke/` — JSON `{"messages":[{"role":"user","content":"..."}],"max_tokens":256}`（需登录 Session）；写入 `LLMCallLog`（Admin 可查看）
- 环境变量：`TC_LLM_PROVIDER`（`mock` \| `openai` \| `dashscope`）、`TC_OPENAI_*`、`TC_DASHSCOPE_*`、`TC_LLM_MAX_OUTPUT_TOKENS`、`TC_LLM_TIMEOUT_SECONDS`

## GitLab（M0-04，读路径）

- `GET /api/health/gitlab/` — 调用 GitLab `GET /api/v4/version`；未配置 URL/Token 时返回 `skipped`
- 可选：`TC_GITLAB_PROJECT_ID` — 额外 `GET /api/v4/projects/:id` 探测项目可读性
- `TC_GITLAB_SSL_VERIFY=0` 仅用于内网自签证书调试

### 写路径演练（阶段 B）

- `POST /api/gitlab/smoke-write/` — 在已配置项目中创建临时分支、单文件提交、并打开 MR（`remove_source_branch=true`）
- 需要 **Session 登录**且用户角色为 **Platform Engineer**；并设置 **`TC_GITLAB_ENABLE_WRITE=1`**（默认关闭，避免误触生产仓库）

## 认证（M0-02）

- `GET /api/auth/csrf/` — 下发 CSRF Cookie（浏览器对接 `/tc` 前调用）
- `POST /api/auth/login/` — JSON `{"username","password"}`，Session 登录
- `POST /api/auth/logout/` — 退出
- `GET /api/me/` — 当前用户与 `role`
- `GET /api/debug/owner-admin-ping/` — 示例：仅 `owner` / `admin` 可访问（验收「角色 × 动作」最小切片）

### 演示账号（内网 / 开发）

```bash
export TC_DEMO_PASSWORD='your-safe-password'
python manage.py seed_builder_demo_users
```

将创建 `tc_owner`、`tc_reviewer`、`tc_admin`、`tc_platform_engineer`、`tc_human_developer` 五个用户并写入对应角色。

## 自动化测试

需要 **Python 3.12+**（与 `Dockerfile` 一致）。本机若无 3.12，可在重建镜像后于容器内运行：

```bash
# 在仓库根目录
docker compose build tc-backend
docker compose run --rm tc-backend python -m pytest
```

## Docker

由仓库根目录 `docker-compose.yml` 中的 `tc-backend` 服务构建本目录 `Dockerfile`。
