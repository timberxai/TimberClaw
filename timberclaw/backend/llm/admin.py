from django.contrib import admin

from .models import LLMCallLog


@admin.register(LLMCallLog)
class LLMCallLogAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "provider",
        "success",
        "prompt_tokens",
        "completion_tokens",
        "latency_ms",
    )
    list_filter = ("provider", "success")
    readonly_fields = (
        "created_at",
        "provider",
        "success",
        "prompt_tokens",
        "completion_tokens",
        "latency_ms",
        "error_message",
    )
