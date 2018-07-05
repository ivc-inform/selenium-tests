from django.test import TestCase


class SendLoginEmailViewTest(TestCase):
    def test_redirects_to_home_page(self):
        response = self.client.post("/accounts/send_login_email/", data=dict(email="test@ivc-inform.ru"))
        self.assertRedirects(response, "/")
