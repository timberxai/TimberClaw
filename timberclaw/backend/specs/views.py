from typing import cast

from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import SpecDocument, SpecVersion
from .serializers import (
    SpecDocumentCreateSerializer,
    SpecDocumentSerializer,
)


class SpecDocumentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """M1-01：已登录用户可列出 / 创建 / 查看自己的 spec 文档草稿。"""

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SpecDocument.objects.filter(created_by=self.request.user).prefetch_related(
            "versions",
        )

    def get_serializer_class(self):
        if self.action == "create":
            return SpecDocumentCreateSerializer
        return SpecDocumentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        doc = cast(SpecDocument, serializer.instance)
        out = SpecDocumentSerializer(doc, context={"request": request})
        return Response(out.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        doc = serializer.save(created_by=self.request.user)
        SpecVersion.objects.create(document=doc, version_number=1, scenario_view="{}")
