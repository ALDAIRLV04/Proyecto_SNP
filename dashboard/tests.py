from django.test import TestCase
from django.urls import reverse
from .models import Muestra


class DashboardTests(TestCase):
    def test_home_status(self):
        Muestra.objects.create(nombre='Test', fecha='2024-01-01', latitud=0, longitud=0)
        response = self.client.get(reverse('dashboard_home'))
        self.assertEqual(response.status_code, 200)