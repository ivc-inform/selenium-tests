from unittest import skip

from django.core.exceptions import ValidationError
from django.test import TestCase

from lists.models import Item, List
from lists.settings import templateListPage, listUrl, message1


class ListViewTest(TestCase):
    def test_uses_list_template(self):
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

        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"], correct_list)

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text="")
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolut_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f"/lists/{list_.id}/")

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f"/lists/{correct_list.id}/", data=dict(item_text=message1))
        self.assertEqual(Item.objects.count(), 1)

        newItem = Item.objects.first()

        self.assertEqual(newItem.text, message1)
        self.assertEqual(newItem.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correctList = List.objects.create()

        response = self.client.post(f"/lists/{correctList.id}/", data=dict(item_text=message1))
        # print(f"response.status_code: {response.status_code}")
        self.assertRedirects(response, f"/lists/{correctList.id}/")
