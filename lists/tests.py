from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

# class SmokeTest(TestCase):
#     def test_bad(self):
#         self.assertEqual(1 + 1, 3)


from lists.views import home_page


class HomePageTest(TestCase):
    def test_root_url(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode("utf-8")
        self.assertTrue(html.startswith("<html>"))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith("</html>"))
