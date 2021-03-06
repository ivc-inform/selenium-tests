from django.shortcuts import render, redirect

from accounts.models import User
from lists.forms import ItemForm, NewListForm
from lists.models import Item, List
from lists.settings import templateListPage, templateHomePage


def home_page(request):
    # print(ItemForm().as_p())
    return render(request, templateHomePage, dict(form=ItemForm()))


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()

    if request.method == "POST":
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)
    return render(request, templateListPage, dict(list=list_, form=form))


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List()
        if request.user.is_authenticated:
            list_.owner = request.user
        list_.save()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, "home.html", dict(form=form))

def new_list2(request):
    form = NewListForm(data=request.POST)
    list_ = form.save(owner=request.user)
    return redirect(str(list_.get_absolute_url()))
    # return redirect(list_)


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, "my_lists.html", dict(owner=owner))
