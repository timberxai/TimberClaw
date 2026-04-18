import time

from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .gateway import invoke_chat
from .models import LLMCallLog
from .redact import redact_text
from .serializers import LLMInvokeSerializer


class HealthLLMView(APIView):
    """配置探测：不发起真实扣费请求（除 mock 外仅检查密钥是否就绪）。"""

    permission_classes = [AllowAny]

    def get(self, request):
        provider = settings.TC_LLM_PROVIDER
        openai_ok = bool(settings.TC_OPENAI_API_KEY)
        dash_ok = bool(settings.TC_DASHSCOPE_API_KEY)
        ready = True
        if provider == "openai" and not openai_ok:
            ready = False
        if provider in ("dashscope", "qwen") and not dash_ok:
            ready = False
        status = "ok" if ready or provider == "mock" else "degraded"
        return Response(
            {
                "status": status,
                "provider": provider,
                "max_output_tokens_cap": settings.TC_LLM_MAX_OUTPUT_TOKENS,
                "timeout_seconds": settings.TC_LLM_TIMEOUT_SECONDS,
                "providers": {
                    "openai": {"api_key_configured": openai_ok},
                    "dashscope": {"api_key_configured": dash_ok},
                },
            },
        )


class LLMInvokeView(APIView):
    """受控调用入口（需登录）；结果写入 LLMCallLog。"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = LLMInvokeSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        messages = [dict(m) for m in ser.validated_data["messages"]]
        max_tokens = ser.validated_data.get("max_tokens")
        provider = settings.TC_LLM_PROVIDER
        start = time.perf_counter()
        try:
            result = invoke_chat(messages, max_output_tokens=max_tokens)
            latency_ms = int((time.perf_counter() - start) * 1000)
            LLMCallLog.objects.create(
                provider=provider,
                success=True,
                prompt_tokens=result.prompt_tokens,
                completion_tokens=result.completion_tokens,
                latency_ms=latency_ms,
            )
            return Response(
                {
                    "text": result.text,
                    "prompt_tokens": result.prompt_tokens,
                    "completion_tokens": result.completion_tokens,
                    "latency_ms": latency_ms,
                },
            )
        except Exception as exc:  # noqa: BLE001 — 边界：记录任意失败原因
            latency_ms = int((time.perf_counter() - start) * 1000)
            LLMCallLog.objects.create(
                provider=provider,
                success=False,
                latency_ms=latency_ms,
                error_message=redact_text(str(exc))[:2000],
            )
            return Response({"detail": redact_text(str(exc))}, status=502)
