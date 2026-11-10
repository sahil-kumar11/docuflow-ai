import secrets
import hashlib
import base64
import requests

from google.oauth2 import id_token
from google.auth.transport.requests import Request as GoogleRequest
from django.http import JsonResponse
from uuid import uuid4
from django.contrib.auth import get_user_model
from django.db import transaction
from core.models import GoogleAccount

from urllib.parse import urlencode
from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.http import require_GET
from rest_framework_simplejwt.tokens import RefreshToken


@require_GET
def google_login(request):
    state = secrets.token_urlsafe(32)
    verifier = secrets.token_urlsafe(64)

    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()
    ).rstrip(b"=").decode()

    request.session["google_oauth_state"] = state
    request.session["google_pkce_verifier"] = verifier

    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }

    url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        + urlencode(params)
    )

    return redirect(url)

@require_GET
def google_callback(request):
    state = request.GET.get("state")
    code = request.GET.get("code")

    saved_state = request.session.pop(
        "google_oauth_state", None
    )
    verifier = request.session.pop(
        "google_pkce_verifier", None
    )

    if (
        not state
        or not saved_state
        or not verifier
        or not code
        or not secrets.compare_digest(state, saved_state)
    ):
        return JsonResponse(
            {"error": "Invalid Google OAuth request"},
            status=400,
        )

    try:
        response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
                "code_verifier": verifier,
            },
            timeout=15,
        )
        response.raise_for_status()

        token = response.json().get("id_token")

        if not token:
            raise ValueError("Missing ID token")

        user_info = id_token.verify_oauth2_token(
            token,
            GoogleRequest(),
            settings.GOOGLE_CLIENT_ID,
        )

        if not user_info.get("email_verified"):
            return JsonResponse(
                {"error": "Google email is not verified"},
                status=403,
            )

        if not user_info.get("sub") or not user_info.get("email"):
            return JsonResponse(
                {"error": "Incomplete Google identity"},
                status=400,
            )

        user = get_or_create_google_user(user_info)

        refresh = RefreshToken.for_user(user)

        return JsonResponse({
            "message": "Google login successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
            },
            "access": str(refresh.access_token),
            "refresh": str(refresh),
})

    except (requests.RequestException, ValueError):
        return JsonResponse(
            {"error": "Google authentication failed"},
            status=400,
        )

@transaction.atomic
def get_or_create_google_user(user_info):
    User = get_user_model()

    google_sub = user_info["sub"]
    email = user_info["email"].strip().lower()

    account = GoogleAccount.objects.filter(
        google_sub=google_sub
    ).select_related("user").first()

    if account:
        if not account.user.is_active:
            raise ValueError("User account is disabled")
        return account.user

    # Never automatically link an existing password account
    if User.objects.filter(email__iexact=email).exists():
        raise ValueError(
            "Existing account requires explicit Google linking"
        )

    user = User.objects.create_user(
        username=f"google_{uuid4().hex}",
        email=email,
        password=None,
    )

    GoogleAccount.objects.create(
        user=user,
        google_sub=google_sub,
    )

    return user

