import json

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from llm.models import LLMCallLog

User = get_user_model()


def _j(response):
    return json.loads(response.content.decode())


@pytest.mark.django_db
def test_health_llm_mock_ok():
    client = Client()
    r = client.get("/api/health/llm/")
    assert r.status_code == 200
    body = _j(r)
    assert body["provider"] == "mock"
    assert body["status"] == "ok"


@pytest.mark.django_db
def test_llm_invoke_mock_creates_log():
    client = Client(enforce_csrf_checks=False)
    u = User.objects.create_user(username="u_llm", password="pw")
    assert client.login(username="u_llm", password="pw")
    r = client.post(
        "/api/llm/invoke/",
        data=json.dumps(
            {"messages": [{"role": "user", "content": "hello"}]},
        ),
        content_type="application/json",
    )
    assert r.status_code == 200
    body = _j(r)
    assert "[mock]" in body["text"]
    assert LLMCallLog.objects.filter(success=True).exists()
