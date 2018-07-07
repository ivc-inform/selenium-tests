from django.conf.global_settings import SESSION_COOKIE_NAME
from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore

from accounts.tests.test_views import EMAIL_TEST
from functional_tests.base import FunctionalTest
from project import settings

User = get_user_model()


class MyListsTest(FunctionalTest):
    def create_pre_autenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=SESSION_COOKIE_NAME,
            value=session.session_key,
            path="/"
        ))

    def test_logged_in_user_lists_are_saved_as_my_lists(self):
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email=EMAIL_TEST)
        self.create_pre_autenticated_session(EMAIL_TEST)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email=EMAIL_TEST)
