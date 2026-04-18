from rest_framework import permissions

from .models import BuilderRole


class IsOwnerOrAdmin(permissions.BasePermission):
    """示例门禁：仅 Owner 或 Admin 可访问（后续替换为完整「动作」矩阵）。"""

    message = "需要 Owner 或 Admin 角色。"

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        profile = getattr(request.user, "builder_profile", None)
        if profile is None:
            return False
        return profile.role in (BuilderRole.OWNER, BuilderRole.ADMIN)
