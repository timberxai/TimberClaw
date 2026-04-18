import json

import pytest
from django.test import Client


def _j(response):
    return json.loads(response.content.decode())


@pytest.mark.django_db
def test_api_health_includes_database_ok():
    client = Client()
    r = client.get("/api/health/")
    assert r.status_code == 200
    body = _j(r)
    assert body["status"] == "ok"
    assert body["service"] == "timberclaw-builder-api"
    assert body["checks"]["database"]["ok"] is True
