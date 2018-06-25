from django.shortcuts import render, redirect

from lists.models import Item, List
from lists.settings import templateListPage, templateHomePage, listUrl


def home_page(request):
    return render(request, templateHomePage)


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, templateListPage, dict(items=items))


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=list_)
    return redirect(f"/{listUrl(list_.id)}")
