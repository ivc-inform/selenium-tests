from unittest import skip

from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    @skip
    def test_cannot_add_empty(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)
        self.wait_forl(lambda: self.assertEqual(self.browser.find_element_by_css_selector(".has_error").text, "You can`t have en empty list item."))
        self.fail("write me !!")
