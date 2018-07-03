from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest

TEST_EMAIL = 'test@ivc-info.ru'
SUBJECT = 'Your login link for Superlists'


class LoginTets(FunctionalTest):
    def test_can_get_email_link_to_log_in(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)
