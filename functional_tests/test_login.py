from accounts.tests.test_views import TEST_EMAIL
from functional_tests.base import FunctionalTest


class LoginTest(FunctionalTest):
    def test_can_get_email_link_to_log_in(self):
        self.wait_to_be_logged_in(email=TEST_EMAIL)
        self.browser.find_element_by_link_text("Log out").click()
        self.wait_to_be_logged_out(email=TEST_EMAIL)
