from django.http import JsonResponse


def health(_request):
    """Liveness probe for compose / M0-05 health checks."""
    return JsonResponse({"status": "ok", "service": "timberclaw-builder-api"})
