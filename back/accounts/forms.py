import datetime

from django import forms

from .validators import validate_birth, validate_names, validate_password, validate_phone, validate_student_id


GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female')
)

class AccountCreateForm(forms.Form):
    username = forms.CharField(max_length=150, validators=[validate_names])
    email = forms.EmailField(max_length=254)
    password = forms.CharField(min_length= 8, max_length=128, validators=[validate_password])
    name = forms.CharField(max_length=18, validators=[validate_names])
    generation = forms.IntegerField(min_value= 1993, max_value=datetime.datetime.now().year)
    student_id = forms.CharField(max_length=12, validators=[validate_student_id])
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    birth = forms.DateField(input_formats=['%Y-%m-%d'], required=False, validators=[validate_birth])
    phone = forms.CharField(max_length=13, required=False, empty_value=None, validators=[validate_phone])


class AccountUpdateForm(forms.Form):
    email = forms.EmailField(max_length=254, required=False)
    password = forms.CharField(min_length= 8, max_length=128, required=False, validators=[validate_password])
    name = forms.CharField(max_length=18, required=False, validators=[validate_names])
    generation = forms.IntegerField(min_value= 1993, max_value=datetime.datetime.now().year, required=False)
    student_id = forms.CharField(max_length=12, required=False, validators=[validate_student_id])
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False)
    birth = forms.DateField(input_formats=['%Y-%m-%d'], required=False, validators=[validate_birth])
    phone = forms.CharField(max_length=13, required=False, empty_value=None, validators=[validate_phone])