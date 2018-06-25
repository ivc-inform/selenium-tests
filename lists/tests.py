from django.test import TestCase
from django.urls import resolve

from lists.models import Item, List
from lists.settings import templateListPage, templateHomePage, listUrl
from lists.views import home_page


class HomePageTest(TestCase):
    def test_root_url(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, templateHomePage)

    # def test_can_have_a_post_count(self):
    #     response = self.client.post("/", data={"item_text": "A new list item"})
    #     self.assertEqual(Item.objects.count(), 1)

    # def test_can_have_a_post_response(self):
    #     response = self.client.post("/", data={"item_text": "A new list item"})
    #     self.assertEqual(Item.objects.count(), 1)
    #     newItem = Item.objects.first()
    #     self.assertEqual(newItem.text, "A new list item")
    #
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response["location"], "/lists/only-single/")

    # def display_all_items(self):
    #     Item.objects.create(text="item 1")
    #     Item.objects.create(text="item 2")
    #
    #     response = self.client.get("/")
    #
    #     self.assertIn("item 1", response.content.decode())
    #     self.assertIn("item 2", response.content.decode())


class ItemModelTest(TestCase):
    def test_saving_and_retriving_items(self):
        list = List()
        list.save()

        firstItem = Item()
        firstItem.text = "Это первая запись"
        firstItem.list = list
        firstItem.save()

        secondItem = Item()
        secondItem.text = "Это вторая запись"
        secondItem.list = list
        secondItem.save()

        savedItems = List.objects.all()
        self.assertEqual(savedItems.count(), 1)

        savedItems = Item.objects.all()
        self.assertEqual(savedItems.count(), 2)

        firstSavedItem = savedItems[0]
        secondSavedItem = savedItems[1]

        self.assertEqual(firstItem.text, "Это первая запись")
        self.assertEqual(firstItem.list, list)
        self.assertEqual(secondItem.text, "Это вторая запись")
        self.assertEqual(secondItem.list, list)


class ListViewTest(TestCase):
    def test_uses_list_templates(self):
        response = self.client.get(f"/{listUrl()}")
        self.assertTemplateUsed(response, "list.html")

    def test_display_all_items(self):
        list = List.objects.create()
        Item.objects.create(text="item 1", list=list)
        Item.objects.create(text="item 2", list=list)

        response = self.client.get(f"/{listUrl()}")

        self.assertContains(response, "item 1")
        self.assertContains(response, "item 2")


class NewListTest(TestCase):

    def setUp(self):
        self.itemText = "A new list item"
        self.dictItemText = dict(item_text=self.itemText)

    def test_can_save_a_POST_request(self):
        response = self.client.post("/lists/new", data=self.dictItemText)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, self.itemText)

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data=self.dictItemText)
        self.assertRedirects(response, f"/{listUrl()}")

class ListViewTest(TestCase):
    def test_users(self):
        list = List.objects.create()
        response = self.client.get(f"/{listUrl(list.id)}")
        self.assertTemplateUsed(response, templateListPage)

    def test_displays_only_items_for_that_list(self):
        correctList = List.objects.create()
        Item.objects.create(text="item 1", list = correctList)
        Item.objects.create(text="item 2", list = correctList)

        anotherList = List.objects.create()
        Item.objects.create(text="another item 1", list=anotherList)
        Item.objects.create(text="another item 2", list=anotherList)

        response = self.client.get(f"/{listUrl(correctList.id)}")

        self.assertContains(response, "item 1")
        self.assertContains(response, "item 2")

        self.assertNotContains(response, "another item 1")
        self.assertNotContains(response, "another item 2")