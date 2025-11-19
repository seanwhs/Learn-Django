# pages/tests.py
from django.test import SimpleTestCase


class HomePageTest(SimpleTestCase):
    def test_url_exist_at_current_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


class AboutPageTest(SimpleTestCase):
    def test_url_exist_at_current_location(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)
