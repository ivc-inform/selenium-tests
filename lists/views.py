from django.http import HttpResponse
from django.shortcuts import render, redirect

from lists.models import Item


# todo Скорректировать модель так, чтобы элементы были связаны с разными списками

def home_page(request):
    return render(request, "home.html")


def view_list(request):
    return render(request, "list.html", dict(items=Item.objects.all()))


def new_list(request):
    Item.objects.create(text=request.POST["item_text"])
    return redirect("/lists/only-single/")
