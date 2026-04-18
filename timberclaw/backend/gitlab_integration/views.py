from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .client import gitlab_project_probe, gitlab_version_payload


class HealthGitLabView(APIView):
    """GitLab 连通性自检（不创建分支 / MR）。"""

    permission_classes = [AllowAny]

    def get(self, request):
        version = gitlab_version_payload()
        project = gitlab_project_probe()
        if version.get("skipped"):
            status = "skipped"
        elif version.get("ok"):
            status = "ok"
        else:
            status = "error"
        body = {
            "status": status,
            "gitlab_url_configured": bool(settings.TC_GITLAB_URL),
            "token_configured": bool(settings.TC_GITLAB_TOKEN),
            "version": version,
        }
        if project is not None:
            body["project"] = project
        return Response(body)
