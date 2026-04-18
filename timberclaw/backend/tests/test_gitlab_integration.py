import json
from unittest.mock import MagicMock, patch

import httpx
import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.test.utils import override_settings

from accounts.models import BuilderRole

User = get_user_model()


def _j(response):
    return json.loads(response.content.decode())


@pytest.fixture
def api_client():
    return Client(enforce_csrf_checks=False)


@pytest.mark.django_db
def test_health_gitlab_skipped_without_env():
    client = Client()
    r = client.get("/api/health/gitlab/")
    assert r.status_code == 200
    body = _j(r)
    assert body["status"] == "skipped"


@pytest.mark.django_db
@override_settings(TC_GITLAB_ENABLE_WRITE=False)
def test_smoke_write_forbidden_when_write_disabled(api_client):
    pe = User.objects.create_user(username="pe_smoke1", password="pw-smoke")
    pe.builder_profile.role = BuilderRole.PLATFORM_ENGINEER
    pe.builder_profile.save()
    assert api_client.login(username="pe_smoke1", password="pw-smoke")
    r = api_client.post("/api/gitlab/smoke-write/")
    assert r.status_code == 403


@pytest.mark.django_db
@override_settings(
    TC_GITLAB_ENABLE_WRITE=True,
    TC_GITLAB_URL="https://gl.example",
    TC_GITLAB_TOKEN="tok",
    TC_GITLAB_PROJECT_ID="42",
)
def test_smoke_write_requires_platform_engineer(api_client):
    owner = User.objects.create_user(username="own_smoke1", password="pw-smoke")
    owner.builder_profile.role = BuilderRole.OWNER
    owner.builder_profile.save()
    assert api_client.login(username="own_smoke1", password="pw-smoke")
    r = api_client.post("/api/gitlab/smoke-write/")
    assert r.status_code == 403


class _FakeResp:
    def __init__(self, data, status_code=200, text=""):
        self._data = data
        self.status_code = status_code
        self.text = text or json.dumps(data)

    def raise_for_status(self):
        if self.status_code >= 400:
            req = MagicMock()
            raise httpx.HTTPStatusError("err", request=req, response=self)

    def json(self):
        return self._data


@pytest.mark.django_db
@override_settings(
    TC_GITLAB_ENABLE_WRITE=True,
    TC_GITLAB_URL="https://gl.example",
    TC_GITLAB_TOKEN="tok",
    TC_GITLAB_PROJECT_ID="42",
)
@patch("gitlab_integration.client.httpx.Client")
def test_smoke_write_success(mock_client_cls, api_client):
    pe = User.objects.create_user(username="pe_smoke2", password="pw-smoke")
    pe.builder_profile.role = BuilderRole.PLATFORM_ENGINEER
    pe.builder_profile.save()
    assert api_client.login(username="pe_smoke2", password="pw-smoke")

    inner = MagicMock()
    inner.get.return_value = _FakeResp({"default_branch": "main"})
    inner.post.side_effect = [
        _FakeResp({"id": "deadbeef", "short_id": "dead"}),
        _FakeResp({"iid": 9, "web_url": "https://gl.example/mr/9"}),
    ]
    mock_client_cls.return_value.__enter__.return_value = inner

    r = api_client.post("/api/gitlab/smoke-write/")
    assert r.status_code == 200
    body = _j(r)
    assert body["ok"] is True
    assert body["commit_short_id"] == "dead"
    assert body["merge_request"]["iid"] == 9
    assert body["source_branch"].startswith("tc/wave-a-smoke-")
    inner.get.assert_called_once()
    assert inner.post.call_count == 2
