from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsPlatformEngineer

from .client import (
    gitlab_project_probe,
    gitlab_smoke_branch_commit_mr,
    gitlab_version_payload,
)


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


class GitLabSmokeWriteView(APIView):
    """GitLab 写路径演练：临时分支 + 提交 + MR（需显式开启 TC_GITLAB_ENABLE_WRITE）。"""

    permission_classes = [IsAuthenticated, IsPlatformEngineer]

    def post(self, request):
        if not settings.TC_GITLAB_ENABLE_WRITE:
            return Response(
                {"detail": "TC_GITLAB_ENABLE_WRITE 未开启（设为 1 后重试）"},
                status=403,
            )
        result = gitlab_smoke_branch_commit_mr()
        if result.get("ok"):
            return Response(result, status=200)
        if result.get("step") == "config":
            return Response(result, status=400)
        return Response(result, status=502)
