"""
   Copyright 2013, 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
__author__ = 'rtubiopa@calpoly.edu'

from django import forms as django_forms
from services.leop.models import leop as leop_models


class LeopForm(django_forms.ModelForm):
    """Form
    Form for creating a manager for the LEOP operations phase.
    """

    tle_l1 = django_forms.RegexField(
        label='TLE - First Line',
        regex=r'^[a-zA-Z0-9.\s-]{69}$',
        error_messages={'invalid': "Not a valid TLE line."}
    )
    tle_l2 = django_forms.RegexField(
        label='TLE - Second Line',
        regex=r'^[a-zA-Z0-9.\s-]{69}$',
        error_messages={'invalid': "Not a valid TLE line."}
    )

    class Meta:
        """Model to be used from within this form."""
        model = leop_models.LEOP
        fields = ('identifier',)