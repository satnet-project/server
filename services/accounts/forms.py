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

from django import forms
from django.core import exceptions
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from . import utils
from services.accounts import models as account_models


class BaseUserProfileForm(forms.ModelForm):
    """
    Base class with common methods for all those forms that deal with the
    UserProfile model.
    """

    def clean_username(self):
        """
        Validate that the username is not already in use.
        """
        existing = User.objects.filter(
            username__iexact=self.cleaned_data['username']
        )

        if existing.exists():
            raise forms.ValidationError(
                _("A user with that username already exists.")
            )
        else:
            return self.cleaned_data['username']

    def clean_email(self):
        """
        Validate that the email is unique in the database and that it is not
        part of a free email provider.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):

            raise forms.ValidationError(
                _("This email address is already in use. Please provide a"
                  "different email address.")
            )

        if BaseUserProfileForm.validate_email(self.cleaned_data['email']):

            return self.cleaned_data['email']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password' in self.cleaned_data\
                and 'password_c' in self.cleaned_data:
            
            if self.cleaned_data['password'] != \
                    self.cleaned_data['password_c']:
                raise forms.ValidationError(
                    _("The two password fields didn't match.")
                )

        return self.cleaned_data


class RegistrationForm(forms.ModelForm):
    """Form for registering a new user in the system.
    """
    class Meta:
        """Model to be used from within this form.
        """
        model = account_models.UserProfile
        fields = (
            'username', 'first_name', 'last_name', 'email',
            'organization', 'country'
        )

    # noinspection PyUnusedLocal
    def signup(self, request, user):
        """(Overriden) save() method for ModelForm.
        This method has to be overriden for saving the UserProfile that
        extends the basic User handled by the Django auth system.
        :param user: User linked with this UserProfile
        :param request: The HTTP request to be processed
        """
        profile = account_models.UserProfile()
        profile.user_ptr = user
        profile.organization = self.cleaned_data['organization']
        profile.country = self.cleaned_data['country']
        profile.blocked = False
        profile.is_verified = False
        profile.save()

        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_superuser = False
        user.is_staff = False
        user.is_active = False
        user.set_password(self.cleaned_data['password1'])
        user.save()


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating the profile of an existing user.
    """
    username = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        """Model to be used from within this form."""
        model = account_models.UserProfile
        fields = (
            'username', 'first_name', 'last_name', 'email',
            'organization', 'country'
        )

    def clean(self):
        """
        The username is not going to be changed, so no further comprobations
        have to be made.
        """
        username = self.cleaned_data['username']
        new_email = self.cleaned_data['email']

        try:
            user = User.objects.get(username=username)
        except exceptions.ObjectDoesNotExist:
            raise forms.ValidationError(
                _(
                    "The given username = <" + username + "> does not exist "
                    "in the database."
                )
            )

        if user.email != new_email:

            utils.validate_email(self.cleaned_data['email'])

            if User.objects.filter(email__iexact=self.cleaned_data['email']):

                raise forms.ValidationError(
                    _(
                        "This email address is already in use. Please provide"
                        "a different email address."
                    )
                )

        return self.cleaned_data
