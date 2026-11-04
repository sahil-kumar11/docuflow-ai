from django.urls import reverse
from rest_framework.test import APITestCase


class HealthCheckTests(APITestCase):

    def test_health_check(self):
        response = self.client.get(
            reverse("health-check")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["status"],
            "ok"
        )