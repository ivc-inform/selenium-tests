from django.forms import Form, CharField, fields


class ItemForm(Form):
    item_text = CharField(
        widget=fields.TextInput(
            attrs={
                "placeholder": "Ввведите задачу",
                "class": "form-control input-lg"
            }
        )
    )
