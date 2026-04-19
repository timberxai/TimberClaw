from django.conf import settings
from django.db import models


class SpecDocument(models.Model):
    """需求 / spec 文档根实体（M1-01 入口落库）。"""

    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="spec_documents",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title


class SpecVersion(models.Model):
    """spec 版本；默认承载「业务场景视图」JSON 文本（M1-02 将由 LLM 填充）。"""

    document = models.ForeignKey(
        SpecDocument,
        on_delete=models.CASCADE,
        related_name="versions",
    )
    version_number = models.PositiveIntegerField()
    scenario_view = models.TextField(blank=True, default="{}")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-version_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["document", "version_number"],
                name="specs_version_unique_per_document",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.document_id} v{self.version_number}"
