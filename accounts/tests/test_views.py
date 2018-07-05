from unittest.mock import patch

from django.test import TestCase

import accounts.views


class SendLoginEmailViewTest(TestCase):
    def test_redirects_to_home_page(self):
        response = self.client.post("/accounts/send_login_email/", data=dict(email="test@ivc-inform.ru"))
        self.assertRedirects(response, "/")

    @patch('accounts.views.send_mail')
    def test_send_mail_to_address_from_post(self, mock_send_mail=None):
        # self.send_mail_called = False

        # def fake_send_mail(subject, body, from_email, to_list):
        #     self.send_mail_called = True
        #     self.subject = subject
        #     self.body = body
        #     self.from_email = from_email
        #     self.to_list = to_list
        #
        # accounts.views.send_mail = fake_send_mail

        self.client.post("/accounts/send_login_email/", data=dict(email="edith@example.com"))
        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, "You login link for List To-Do")
        self.assertEqual(from_email, "noreplay@superlists")
        self.assertEqual(to_list, ["edith@example.com"])

    def test_adds_success_message(self):
        response = self.client.post("/accounts/send_login_email/", data=dict(email="test@ivc-inform.ru"), follow=True)
        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            "Проверьте свою почту, мы отправили Вам ссылку, которую можно использовать для входа на сайт"
        )
        self.assertEqual(message.tags, "success")


class LoginViewTest(TestCase):
    def test_redirects_to_home_page(self):
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response, "/")
