from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, MeSerializer
from .permissions import IsOwnerOrAdmin


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfCookieView(APIView):
    """为浏览器 Session 登录准备 CSRF Cookie（后续 `/tc` 前端对接时使用）。"""

    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"detail": "ok"})


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=ser.validated_data["username"],
            password=ser.validated_data["password"],
        )
        if user is None:
            return Response({"detail": "用户名或密码错误。"}, status=400)
        login(request, user)
        return Response(MeSerializer(user).data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "ok"})


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(MeSerializer(request.user).data)


class OwnerAdminPingView(APIView):
    """用于验收「角色 × 动作」最小示例。"""

    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get(self, request):
        return Response({"detail": "owner-or-admin"})
