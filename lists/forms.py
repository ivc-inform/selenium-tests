from django.forms import ModelForm, TextInput

from lists.models import Item

EMPTY_ITEM_ERROR = 'You can`t have an empty list item'
PLACE_HOLDER = "Ввведите текст задачи"


class ItemForm(ModelForm):
    def save(self, for_list):
        self.instance.list = for_list
        return super().save()

    class Meta:
        model = Item
        fields = ("text",)

        widgets = {
            "text": TextInput(
                attrs={
                    "placeholder": PLACE_HOLDER,
                    "class": "form-control input-lg"
                }
            )
        }

        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }
