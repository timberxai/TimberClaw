import json

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client

from accounts.models import BuilderRole

User = get_user_model()


def _j(response):
    return json.loads(response.content.decode())


@pytest.fixture
def api_client():
    return Client(enforce_csrf_checks=False)


@pytest.mark.django_db
def test_csrf_cookie_endpoint(api_client):
    r = api_client.get("/api/auth/csrf/")
    assert r.status_code == 200


@pytest.mark.django_db
def test_login_me_and_role_gate(api_client):
    owner = User.objects.create_user(username="owner1", password="secret-pw")
    owner.builder_profile.role = BuilderRole.OWNER
    owner.builder_profile.save()

    r = api_client.post(
        "/api/auth/login/",
        data=json.dumps(
            {"username": "owner1", "password": "secret-pw"},
        ),
        content_type="application/json",
    )
    assert r.status_code == 200
    body = _j(r)
    assert body["username"] == "owner1"
    assert body["role"] == BuilderRole.OWNER

    r2 = api_client.get("/api/me/")
    assert r2.status_code == 200
    assert _j(r2)["role"] == BuilderRole.OWNER

    r3 = api_client.get("/api/debug/owner-admin-ping/")
    assert r3.status_code == 200
    assert _j(r3)["detail"] == "owner-or-admin"


@pytest.mark.django_db
def test_reviewer_denied_owner_admin_ping(api_client):
    rev = User.objects.create_user(username="rev1", password="secret-pw")
    rev.builder_profile.role = BuilderRole.REVIEWER
    rev.builder_profile.save()
    assert api_client.login(username="rev1", password="secret-pw")
    r = api_client.get("/api/debug/owner-admin-ping/")
    assert r.status_code == 403


@pytest.mark.django_db
def test_seed_builder_demo_users_command():
    call_command("seed_builder_demo_users")
    assert User.objects.filter(username="tc_owner").exists()
    assert (
        User.objects.get(username="tc_reviewer").builder_profile.role
        == BuilderRole.REVIEWER
    )
