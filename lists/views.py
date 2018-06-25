from django.shortcuts import render, redirect

from lists.models import Item, List

def home_page(request):
    return render(request, "home.html")


def view_list(request):
    return render(request, "list.html", dict(items=Item.objects.all()))


def new_list(request):
    list = List.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=list)
    return redirect("/lists/only-single/")
