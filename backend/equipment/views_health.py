from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def health_check(request):
    """
    Health check endpoint for Render.com
    Returns 200 OK if the service is healthy
    """
    return JsonResponse({
        'status': 'healthy',
        'service': 'chemical-equipment-api',
        'version': '1.0.0'
    })
