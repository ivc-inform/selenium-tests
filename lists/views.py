from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from lists.models import Item, List
from lists.settings import templateListPage, templateHomePage, listUrl


def home_page(request):
    return render(request, templateHomePage, dict(form=ItemForm()))


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)

    if request.method == "POST":
        Item.objects.create(text=request.POST["text"], list=list_)
        return redirect(f"/lists/{list_.id}/")
    return render(request, templateListPage, dict(list=list_))


def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST["text"], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        return render(request, "home.html", dict(error=EMPTY_ITEM_ERROR))
    else:
        return redirect(list_)
