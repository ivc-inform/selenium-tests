import os
import poplib
import re
import time

from django.core import mail
from selenium.webdriver.common.keys import Keys

from accounts.tests.test_views import EMAIL_TEST
from functional_tests.base import FunctionalTest

SUBJECT = 'You login link for List To-Do'


class LoginTets(FunctionalTest):
    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(subject, email.subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL("mail.hostland.ru")
        print(inbox.getwelcome())
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['TEST_BOX_PASS'])
            while time.time() - start < 60:
                count, _ = inbox.stat()
                print(f"count:{count}")
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    print(lines)
                    if f"Subject: {subject}" in lines:
                        email_id = i
                        body = "\n".join(lines)
                        return body
                time.sleep(5)

        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

    def test_can_get_email_link_to_log_in(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(EMAIL_TEST)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertIn('Проверьте свою почту, мы отправили Вам ссылку, которую можно использовать для входа на сайт', self.browser.find_element_by_tag_name('body').text))

        print("point 1")
        body = self.wait_for_email(EMAIL_TEST, SUBJECT)
        print("point 2")

        self.assertIn("Use this link to log in", body)
        print("point 3")
        url_search = re.search(r"http://.+/.+$", body)
        print("point 4")

        if not url_search:
            self.fail(f"Could not find url in email body:\n{body}")

        url = url_search.group(0)
        print("point 5")
        self.assertIn(self.live_server_url, url)
        print("point 6")

        print("url", url)
        self.browser.get(url)
        print("point 7")
        self.wait_to_be_logged_in(email=EMAIL_TEST)
        self.browser.find_element_by_link_text("Log out").click()
        self.wait_to_be_logged_out(email=EMAIL_TEST)

if __name__ == '__main__':
    import getpass, poplib

    M = poplib.POP3_SSL('mail.hostland.ru')
    M.user("test@ivc-inform.ru")
    M.pass_("mt30718tm")
    numMessages = len(M.list()[1])
    for i in range(numMessages):
        for j in M.retr(i + 1)[1]:
            print(j)