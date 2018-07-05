import re

from django.core import mail
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest

TEST_EMAIL = 'test@ivc-info.ru'
SUBJECT = 'You login link for List To-Do'


class LoginTets(FunctionalTest):
    def test_can_get_email_link_to_log_in(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        self.wait_forl(lambda: self.assertIn('Проверьте свою почту, мы отправили Вам ссылку, которую можно использовать для входа на сайт', self.browser.find_element_by_tag_name('body').text))

        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        self.assertIn("Use this link to log in", email.body)
        url_search = re.search(r"http://.+/.+$", email.body)
        if not url_search:
            self.fail(f"Could not find url in email body:\n{email.body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        self.browser.get(url)

        self.wait_forl(lambda: self.browser.find_element_by_link_text("Log out"))
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertIn(TEST_EMAIL, navbar.text)
