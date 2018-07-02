from unittest import skip

from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    @skip
    def test_cannot_add_empty(self):
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_forl(lambda: self.assertEqual(self.browser.find_element_by_css_selector(".has_error").text, "You can`t have en empty list item."))

        inputbox = self.get_item_input_box()
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: Buy milk")

        inputbox.send_keys(Keys.ENTER)
        self.wait_forl(lambda: self.assertEqual(self.browser.find_element_by_css_selector(".has_error").text, "You can`t have en empty list item."))

        inputbox.send_keys("Make tea")
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: Buy milk")
        self.wait_for_row_in_list_table("2: Make tea")