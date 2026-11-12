from rest_framework.permissions import BasePermission
from organizations.models import Membership


# Role hierarchy
ROLE_RANK = {
    "EMPLOYEE": 1,
    "MANAGER": 2,
    "ADMIN": 3,
}

# Minimum role required for each action
PERMS = {
    "org.manage_members": "ADMIN",
    "document.delete": "ADMIN",
    "document.upload": "MANAGER",
    "approval.decide": "MANAGER",
    "analytics.view": "MANAGER",
    "document.read": "EMPLOYEE",
    "chat.ask": "EMPLOYEE",
}

class IsOrgMember(BasePermission):
    message = "You are not an active member of this organization."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        org_id = view.kwargs.get("org_id")

        if not org_id:
            return False

        membership = Membership.objects.filter(
            user=request.user,
            organization_id=org_id,
            status=Membership.Status.ACTIVE,
        ).first()

        request.membership = membership

        return membership is not None

def require_role(min_role):
    if min_role not in ROLE_RANK:
        raise ValueError(f"Unknown role: {min_role}")

    class RolePermission(IsOrgMember):
        message = f"This action requires {min_role} role or higher."

        def has_permission(self, request, view):
            if not super().has_permission(request, view):
                return False

            user_role = request.membership.role

            return ROLE_RANK.get(user_role, 0) >= ROLE_RANK[min_role]

    RolePermission.__name__ = f"Requires{min_role.title()}"

    return RolePermission