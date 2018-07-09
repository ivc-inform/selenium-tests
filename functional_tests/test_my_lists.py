from django.contrib.auth import get_user_model

from accounts.tests.test_views import EMAIL_TEST
from functional_tests.base import FunctionalTest

User = get_user_model()


class MyListsTest(FunctionalTest):
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        self.create_pre_authenticated_session(EMAIL_TEST)

        self.browser.get(self.live_server_url)

        self.add_list_item("Reticulate splines")
        self.add_list_item("Immanentize eschaton")
        first_list_url = self.browser.current_url

        self.browser.find_element_by_link_text("My lists").click()

        self.wait_for(lambda: self.browser.find_element_by_link_text("Reticulate splines"))

        self.browser.find_element_by_link_text("Reticulate splines").click()

        self.wait_for(lambda: self.assertEqual(self.browser.current_url, first_list_url))

        self.browser.get(self.live_server_url)
        self.add_list_item("Click cows")

        second_list_url = self.browser.current_url
        self.browser.find_element_by_link_text("My lists").click()
        self.wait_for(lambda: self.browser.find_element_by_link_text("Click cows"))
        self.browser.find_element_by_link_text("Click cows").click()

        self.wait_for(lambda: self.assertEqual(self.browser.current_url, second_list_url))

        self.browser.find_element_by_link_text("Log out").click()

        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_link_text("My lists")))
