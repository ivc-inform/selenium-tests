from django.shortcuts import render, redirect

from lists.models import Item, List
from lists.settings import templateListPage, templateHomePage, listUrl


def home_page(request):
    return render(request, templateHomePage)


def view_list(request):
    return render(request, templateListPage, dict(items=Item.objects.all()))


def new_list(request):
    list = List.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=list)
    return redirect(f"/{listUrl()}")
