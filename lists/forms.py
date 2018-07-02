from django.forms import forms, Form, CharField, fields


class ItemForm(Form):
    item_text = CharField(
        widget= fields.TextInput(
            attrs = dict(placeholder="Ввведите задачу")
        )
    )
