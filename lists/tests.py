from django.test import TestCase
from django.urls import resolve

from lists.models import Item
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

    def test_can_have_a_post_count(self):
        response = self.client.post("/", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)


    def test_can_have_a_post_response(self):
        response = self.client.post("/", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        newItem = Item.objects.first()
        self.assertEqual(newItem.text, "A new list item")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/lists/only-single/")

    def display_all_items(self):
        Item.objects.create(text="item 1")
        Item.objects.create(text="item 2")

        response = self.client.get("/")

        self.assertIn("item 1", response.content.decode())
        self.assertIn("item 2", response.content.decode())


class ItemModelTest(TestCase):
    def test_saving_and_retriving_items(self):
        firstItem = Item()
        firstItem.text = "Это первая запись"
        firstItem.save()

        secondItem = Item()
        secondItem.text = "Это вторая запись"
        secondItem.save()

        savedItems = Item.objects.all()
        self.assertEqual(savedItems.count(), 2)

        firstSavedItem = savedItems[0]
        secondSavedItem = savedItems[1]

        self.assertEqual(firstItem.text, "Это первая запись")
        self.assertEqual(secondItem.text, "Это вторая запись")

class ListViewTest(TestCase):
    def display_all_items(self):
        Item.objects.create(text="item 1")
        Item.objects.create(text="item 2")

        response = self.client.get("/lists/only-single/")

        self.assertContains(response, "item 1")
        self.assertContains(response, "item 2")