from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health_check(request):
    return Response({
        "status": "ok",
        "service": "DocuFlow AI",
        "message": "Django backend is running!",
        "version": "0.1.0"
    })