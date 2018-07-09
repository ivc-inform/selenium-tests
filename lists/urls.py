from django.urls import path

from lists.views import view_list, new_list, my_lists

urlpatterns = [
    path('new', new_list, name="new_list"),
    path('<int:list_id>/', view_list, name="view_list"),
    path('users/<str:email>/', my_lists, name="my_lists"),
]
