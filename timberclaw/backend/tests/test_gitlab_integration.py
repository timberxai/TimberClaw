import json

import pytest
from django.test import Client


def _j(response):
    return json.loads(response.content.decode())


@pytest.mark.django_db
def test_health_gitlab_skipped_without_env():
    client = Client()
    r = client.get("/api/health/gitlab/")
    assert r.status_code == 200
    body = _j(r)
    assert body["status"] == "skipped"
