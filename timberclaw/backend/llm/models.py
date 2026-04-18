from django.db import models


class LLMCallLog(models.Model):
    """出站 LLM 调用的最小审计行（PRD §8.5：用量与失败原因）。"""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    provider = models.CharField(max_length=32)
    success = models.BooleanField(default=False)
    prompt_tokens = models.PositiveIntegerField(default=0)
    completion_tokens = models.PositiveIntegerField(default=0)
    latency_ms = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True, default="")

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "LLM 调用记录"
        verbose_name_plural = "LLM 调用记录"
