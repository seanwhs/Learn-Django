from django.test import SimpleTestCase
from django.urls import reverse

class HomePageTests(SimpleTestCase):
    def test_url_exists_at_current_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_template_content(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, '<h1>Home Page</h1>')

class AboutPageTests(SimpleTestCase):
    def test_url_exists_at_current_location(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_template_content(self):
        response = self.client.get(reverse('about'))
        self.assertContains(response, '<h1>About Page</h1>')