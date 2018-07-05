from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
def send_login_email(request):
    email = request.POST["email"]
    print(type(send_mail))
    send_mail(
        'You login link for List To-Do',
        'Use this link to log in',
        'noreplay@superlists',
        [email]
    )
    messages.success(request, "Проверьте свою почту, мы отправили Вам ссылку, которую можно использовать для входа на сайт")
    return redirect("/")
