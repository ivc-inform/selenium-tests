from django.test import TestCase
from django.urls import resolve

from lists.settings import templateHomePage
from lists.views import home_page


class TestHomePage(TestCase):
    def test_root_url(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, templateHomePage)
