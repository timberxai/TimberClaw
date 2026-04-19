import json

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()


def _j(response):
    return json.loads(response.content.decode())


@pytest.fixture
def api_client():
    return Client(enforce_csrf_checks=False)


@pytest.mark.django_db
def test_specs_documents_requires_login(api_client):
    r = api_client.get("/api/specs/documents/")
    assert r.status_code == 403


@pytest.mark.django_db
def test_specs_create_list_roundtrip(api_client):
    u = User.objects.create_user(username="spec_owner", password="pw-spec")
    assert api_client.login(username="spec_owner", password="pw-spec")
    r = api_client.post(
        "/api/specs/documents/",
        data=json.dumps({"title": "离散制造试点"}),
        content_type="application/json",
    )
    assert r.status_code == 201
    created = _j(r)
    assert created["title"] == "离散制造试点"
    assert len(created["versions"]) == 1
    assert created["versions"][0]["version_number"] == 1

    r2 = api_client.get("/api/specs/documents/")
    assert r2.status_code == 200
    body = _j(r2)
    assert len(body) == 1
    assert body[0]["title"] == "离散制造试点"
