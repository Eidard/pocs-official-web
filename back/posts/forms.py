from django import forms

from .validators import validate_tags


class PostFormExceptFiles(forms.Form):
    title = forms.CharField(max_length=256)
    md_content = forms.CharField()
    background_image_url = forms.ImageField(required=False)
    board_id = forms.IntegerField(min_value=1)
    tags = forms.CharField(required=False, validators=[validate_tags])