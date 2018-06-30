from django.test import TestCase
from django.utils.html import escape

from lists.models import Item, List
from lists.settings import templateListPage, listUrl, message1


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

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post("/lists/new", data=dict(item_text=""))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        expected_error = "You can`t have an empty list item."
        self.assertContains(response, expected_error)

    def test_ivalid_list_items_arent_saved(self):
        self.client.post("/lists/new", data=dict(item_text=""))
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


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
