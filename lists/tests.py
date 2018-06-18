from django.test import TestCase
from django.urls import resolve


# class SmokeTest(TestCase):
#     def test_bad(self):
#         self.assertEqual(1 + 1, 3)


from lists.views import home_page


class HomePageTest(TestCase):
    def test_root_url(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)
