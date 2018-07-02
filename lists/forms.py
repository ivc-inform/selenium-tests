from django.forms import ModelForm, TextInput

from lists.models import Item

EMPTY_ITEM_ERROR = 'You can`t have an empty list item'
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

        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }
