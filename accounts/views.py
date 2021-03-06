import sys

from django.contrib import messages, auth
from django.core.mail import send_mail
from django.shortcuts import redirect

from accounts.models import Token


def send_login_email(request):
    email = request.POST["email"]
    # print(type(send_mail))
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri('login?token=' + str(token.uid))
    send_mail(
        'You login link for List To-Do',
        f'Use this link to log in: \n\n {url}',
        'noreplay@superlists',
        [email]
    )
    messages.success(request, "Проверьте свою почту, мы отправили Вам ссылку, которую можно использовать для входа на сайт")
    return redirect("/")


def login(request):
    print('login view', file=sys.stderr)
    uid = request.GET.get('token')
    user = auth.authenticate(uid=uid)
    if user:
        auth.login(request, user)
    return redirect("/")
