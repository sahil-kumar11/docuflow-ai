from django.contrib import admin
from .models import Organization, Membership


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "created_by",
        "created_at",
    )
    search_fields = ("name", "slug")


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "user",
        "role",
        "status",
        "created_at",
    )
    list_filter = ("role", "status")
    search_fields = ("organization__name", "invite_email")