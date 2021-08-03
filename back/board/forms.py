from django import forms

class BoardForm(forms.Form):
    name = forms.CharField(max_length=128)
    description = forms.CharField(max_length=2048, required=False, empty_value=None)
    board_category_id = forms.IntegerField(min_value=1)


class BoardCategoryForm(forms.Form):
    name = forms.CharField(max_length=64)
    parent_board_category_id = forms.IntegerField(min_value=1, required=False)
