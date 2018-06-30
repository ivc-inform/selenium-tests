from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from lists.models import Item, List
from lists.settings import templateListPage, templateHomePage, listUrl


def home_page(request):
    return render(request, templateHomePage)


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, templateListPage, dict(list=list_))


def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST["item_text"], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        return render(request, "home.html", dict(error = 'You can`t have an empty list item.'))
    else:
        return redirect('view_list', list_.id)


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["item_text"], list = list_)
    return redirect(f"/{listUrl(list_.id)}")
