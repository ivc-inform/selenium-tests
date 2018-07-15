from unittest import skip
from unittest.mock import patch, Mock

from django.http import HttpRequest
from django.test import TestCase

from accounts.models import User
from lists.forms import EMPTY_ITEM_ERROR, ItemForm
from lists.models import Item, List
from lists.settings import listUrl
from lists.views import new_list2


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


class NewListViewIntegratedTest(TestCase):

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

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_ivalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_ivalid_input()
        self.assertContains(response, EMPTY_ITEM_ERROR)

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

    @skip
    def test_list_owner_is_saved_if_user_is_autenticated(self):
        user = User.objects.create(email="a@b.com")
        self.client.force_login(user)
        self.client.post("/lists/new", data=dict(text="new_item"))
        list_ = List.objects.first()
        self.assertEqual(list_.owner, user)


class MyListsTest(TestCase):
    def test_my_lists_url_renders_my_lists_template(self):
        User.objects.create(email="a@b.com")
        response = self.client.get("/lists/users/a@b.com/")
        self.assertTemplateUsed(response, "my_lists.html")

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email="wrong@owner.com")
        correct_user = User.objects.create(email="a@b.com")
        response = self.client.get("/lists/users/a@b.com/")
        self.assertEqual(response.context['owner'], correct_user)

@patch("lists.views.NewListForm")
class NewListViewUnitTest(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.request.POST["text"] = "new list item"
        self.request.user = Mock()

    def test_passes_POST_data_to_NewListForm(self, mockNewListForm):
        new_list2(self.request)
        mockNewListForm.assert_called_once_with(data=self.request.POST)

    def test_saves_from_with_owner_if_form_valid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        new_list2(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch("lists.views.redirect")
    def test_redirects_to_form_returned_object_if_form_valid(self, mock_redirect, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True

        response = new_list2(self.request)
        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(mock_form.save.return_value)
