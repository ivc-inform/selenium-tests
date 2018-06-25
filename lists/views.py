from django.http import HttpResponse
from django.shortcuts import render, redirect

from lists.models import Item

# todo Скорректировать модель так, чтобы элементы были связаны с разными списками

def home_page(request):
    "Домашняя страница"
    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"])
        return redirect("/lists/only-single/")

    items = Item.objects.all()
    return render(request, "home.html", {"items": items})
