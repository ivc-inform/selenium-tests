from django.test import TestCase
from django.utils.html import escape

from lists.forms import EMPTY_ITEM_ERROR
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
        self.dictItemText = dict(text=self.itemText)

    def post_ivalid_input(self):
        list_ = List.objects.create()
        return self.client.post(f"/lists/{list_.id}/", data=dict(text=""))

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_ivalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_render_list_template(self):
        response = self.post_ivalid_input()
        self.assertEqual(response.status_code, 200)

    def test_can_save_a_POST_request(self):
        response = self.client.post("/lists/new", data=self.dictItemText)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, self.itemText)

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data=self.dictItemText)
        newList = List.objects.first()
        self.assertRedirects(response, f"/{listUrl(newList.id)}")

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post("/lists/new", data=dict(text=""))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post("/lists/new", data=dict(text=""))
        self.assertContains(response, EMPTY_ITEM_ERROR)

    def test_ivalid_list_items_arent_saved(self):
        self.client.post("/lists/new", data=dict(text=""))
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
