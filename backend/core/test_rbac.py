# Day 12 - RBAC Automated Tests

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from organizations.models import Organization, Membership


class RBACTests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.admin = User.objects.create_user(
            username="rbac_admin",
            password="TestPass123!",
        )

        self.manager = User.objects.create_user(
            username="rbac_manager",
            password="TestPass123!",
        )

        self.employee = User.objects.create_user(
            username="rbac_employee",
            password="TestPass123!",
        )

        self.outsider = User.objects.create_user(
            username="rbac_outsider",
            password="TestPass123!",
        )

        self.organization = Organization.objects.create(
            name="RBAC Test Organization",
            slug="rbac-test-org",
            created_by=self.admin,
        )

        for user, role in [
            (self.admin, Membership.Role.ADMIN),
            (self.manager, Membership.Role.MANAGER),
            (self.employee, Membership.Role.EMPLOYEE),
        ]:
            Membership.objects.create(
                organization=self.organization,
                user=user,
                role=role,
                status=Membership.Status.ACTIVE,
            )

        self.url = reverse(
            "rbac-check",
            kwargs={"org_id": self.organization.id},
        )

    def test_admin_allowed(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manager_allowed(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_denied(self):
        self.client.force_authenticate(user=self.employee)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_outsider_denied(self):
        self.client.force_authenticate(user=self.outsider)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_inactive_member_denied(self):
        Membership.objects.filter(
            organization=self.organization,
            user=self.manager,
        ).update(status=Membership.Status.REMOVED)

        self.client.force_authenticate(user=self.manager)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_denied(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )