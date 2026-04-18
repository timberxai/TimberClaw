from django.db import connection
from django.http import JsonResponse


def health(_request):
    """Liveness + 默认数据库连通（compose / M0-05）。"""
    db_ok = True
    db_detail: str | None = None
    try:
        connection.ensure_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception as exc:  # noqa: BLE001
        db_ok = False
        db_detail = str(exc)[:500]

    body = {
        "status": "ok" if db_ok else "error",
        "service": "timberclaw-builder-api",
        "checks": {
            "database": {"ok": db_ok, **({"detail": db_detail} if db_detail else {})},
        },
    }
    return JsonResponse(body, status=200 if db_ok else 503)
