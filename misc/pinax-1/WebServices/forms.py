from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django_countries import countries

import account.forms

class SignupForm(account.forms.SignupForm):

    organization = forms.CharField(
        label=_("Organization"),
        max_length=50,
        widget=forms.TextInput(),
        required=True
    )
    
    country = forms.ChoiceField(
        label=_("Country"),
        choices=countries.COUNTRIES,
        widget=forms.Select(),
        required=True
    )

