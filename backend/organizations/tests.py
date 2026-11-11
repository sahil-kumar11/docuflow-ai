from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import Organization, Membership


class OrganizationMembershipTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_admin",
            password="TestPass123!",
        )

        self.org = Organization.objects.create(
            name="DocuFlow Test",
            slug="docuflow-test",
            created_by=self.user,
        )

    def test_organization_creation(self):
        self.assertEqual(self.org.name, "DocuFlow Test")

    def test_membership_creation(self):
        member = Membership.objects.create(
            organization=self.org,
            user=self.user,
            role=Membership.Role.ADMIN,
            status=Membership.Status.ACTIVE,
        )

        self.assertEqual(member.role, "ADMIN")
        self.assertEqual(member.status, "ACTIVE")

    def test_duplicate_membership_blocked(self):
        Membership.objects.create(
            organization=self.org,
            user=self.user,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Membership.objects.create(
                    organization=self.org,
                    user=self.user,
                )

        self.assertEqual(Membership.objects.count(), 1)

    def test_user_can_join_multiple_organizations(self):
        second_org = Organization.objects.create(
            name="Second Organization",
            slug="second-org",
            created_by=self.user,
        )

        Membership.objects.create(
            organization=self.org,
            user=self.user,
        )

        Membership.objects.create(
            organization=second_org,
            user=self.user,
        )

        self.assertEqual(
            Membership.objects.filter(user=self.user).count(),
            2,
        )