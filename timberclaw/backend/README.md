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

健康检查：`GET /api/health/`

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
docker compose run --rm tc-backend pytest
```

## Docker

由仓库根目录 `docker-compose.yml` 中的 `tc-backend` 服务构建本目录 `Dockerfile`。
