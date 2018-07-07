from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token
from accounts.tests.test_views import TEST_EMAIL

User = get_user_model()


class AuthenticateTest(TestCase):
    def test_returns_None_if_no_such_token(self):
        result = PasswordlessAuthenticationBackend().authenticate("no-such-token")
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_tokken_exists(self):
        token = Token.objects.create(email=TEST_EMAIL)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        new_user = User.objects.get(email=TEST_EMAIL)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_emaail_if_token_exists(self):
        existing_user = User.objects.create(email=TEST_EMAIL)
        token = Token.objects.create(email=TEST_EMAIL)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        self.assertEqual(user, existing_user)


    def test_get_user_by_email(self):
        self.assertIsNone(PasswordlessAuthenticationBackend().get_user(TEST_EMAIL))