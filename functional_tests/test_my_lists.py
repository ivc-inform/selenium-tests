from django.conf.global_settings import SESSION_COOKIE_NAME
from django.contrib.auth import get_user_model

from accounts.tests.test_views import EMAIL_TEST
from functional_tests.base import FunctionalTest
from functional_tests.management.commands.create_session import create_pre_autenticated_session
from functional_tests.server_tools import create_session_on_server

User = get_user_model()


class MyListsTest(FunctionalTest):
    def create_pre_autenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_autenticated_session(email)

        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=SESSION_COOKIE_NAME,
            value=session_key,
            path="/"
        ))

    def test_logged_in_user_lists_are_saved_as_my_lists(self):
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email=EMAIL_TEST)
        self.create_pre_autenticated_session(EMAIL_TEST)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email=EMAIL_TEST)
