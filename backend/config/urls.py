from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from core.google_oauth import google_login , google_callback

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
    path("api/health/", lambda request: JsonResponse({"status": "ok"})),
    path("api/auth/google/login/", google_login, name="google_login"),
    path("api/auth/google/callback/", google_callback, name="google_callback"),
]