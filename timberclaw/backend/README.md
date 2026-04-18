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

## Docker

由仓库根目录 `docker-compose.yml` 中的 `tc-backend` 服务构建本目录 `Dockerfile`。
