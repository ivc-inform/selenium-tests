from django.forms import ModelForm, TextInput

from lists.models import Item


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ("text",)

        widgets = {
            "text": TextInput(
                attrs={
                    "placeholder": "Ввведите задачу",
                    "class": "form-control input-lg"
                }
            )
        }
