from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.permissions import require_role


class RBACCheckView(APIView):
    permission_classes = [
        IsAuthenticated,
        require_role("MANAGER"),
    ]

    def get(self, request, org_id):
        return Response({
            "message": "RBAC access granted",
            "organization_id": str(org_id),
            "your_role": request.membership.role,
        })