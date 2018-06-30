from django.test import TestCase

from lists.models import Item, List
from lists.settings import templateListPage, listUrl, message1

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


