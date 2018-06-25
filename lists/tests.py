from django.test import TestCase
from django.urls import resolve

from lists.models import Item, List
from lists.settings import templateListPage, templateHomePage, listUrl, message1
from lists.views import home_page


class HomePageTest(TestCase):
    def test_root_url(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, templateHomePage)


class ItemModelTest(TestCase):
    def test_saving_and_retriving_items(self):
        list_ = List()
        list_.save()

        firstItem = Item()
        firstItem.text = "Это первая запись"
        firstItem.list = list_
        firstItem.save()

        secondItem = Item()
        secondItem.text = "Это вторая запись"
        secondItem.list = list_
        secondItem.save()

        savedItems = List.objects.all()
        self.assertEqual(savedItems.count(), 1)

        savedItems = Item.objects.all()
        self.assertEqual(savedItems.count(), 2)

        firstSavedItem = savedItems[0]
        secondSavedItem = savedItems[1]

        self.assertEqual(firstItem.text, "Это первая запись")
        self.assertEqual(firstItem.list, list_)
        self.assertEqual(secondItem.text, "Это вторая запись")
        self.assertEqual(secondItem.list, list_)


class ListViewTest(TestCase):
    def test_uses_list_templates(self):
        response = self.client.get(f"/{listUrl()}")
        self.assertTemplateUsed(response, "list.html")

    def test_display_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text="item 1", list=list_)
        Item.objects.create(text="item 2", list=list_)

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
        newList = List.objects.first()
        self.assertRedirects(response, f"/{listUrl(newList.id)}")


class ListViewTest(TestCase):
    def test_users(self):
        list_ = List.objects.create()
        response = self.client.get(f"/{listUrl(list_.id)}")
        self.assertTemplateUsed(response, templateListPage)

    def test_displays_only_items_for_that_list(self):
        correctList = List.objects.create()
        Item.objects.create(text="item 1", list=correctList)
        Item.objects.create(text="item 2", list=correctList)

        anotherList = List.objects.create()
        Item.objects.create(text="another item 1", list=anotherList)
        Item.objects.create(text="another item 2", list=anotherList)

        response = self.client.get(f"/{listUrl(correctList.id)}")

        self.assertContains(response, "item 1")
        self.assertContains(response, "item 2")

        self.assertNotContains(response, "another item 1")
        self.assertNotContains(response, "another item 2")

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"], correct_list)


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f"/lists/{correct_list.id}/add_item", data=dict(item_text=message1))
        self.assertEqual(Item.objects.count(), 1)

        newItem = Item.objects.first()

        self.assertEqual(newItem.text, message1)
        self.assertEqual(newItem.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correctList = List.objects.create()

        response = self.client.post(f"/{listUrl(correctList.id)}add_item", data=dict(item_text=message1))
        self.assertRedirects(response, f"/{listUrl(correctList.id)}")
