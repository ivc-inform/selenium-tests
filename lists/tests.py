from django.test import TestCase
from django.test import TestCase
from django.urls import resolve

from lists.views import home_page


# class SmokeTest(TestCase):
#     def test_bad(self):
#         self.assertEqual(1 + 1, 3)


class HomePageTest(TestCase):
    def test_root_url(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_can_have_a_post_response(self):
        response = self.client.post("/", data={"item_text": "A new list item"})
        self.assertIn("A new list item", response.content.decode())
        self.assertTemplateUsed(response, "home.html")
