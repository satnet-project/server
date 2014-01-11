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

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from accounts.models import UserProfile
from passwords.fields import PasswordField


class BaseUserProfileForm(ModelForm):
    """
    Base class with common methods for all those forms that deal with the
    UserProfile model.
    """

    def clean_username(self):
        """
        Validate that the username is not already in use.
        """
        
        existing = User.objects\
            .filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms\
                .ValidationError(_("A user with that username already exists."))
        else:
            return self.cleaned_data['username']

    #Flag that controls whether an account from a free-registration email
    #service can be used for registering within the system or not.
    check_domains = False
    
    # To change the list of banned domains, subclass this form and
    # override the attribute ``bad_domains``.
    bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
                   'googlemail.com', 'hotmail.com', 'hushmail.com',
                   'msn.com', 'mail.ru', 'mailinator.com', 'live.com',
                   'yahoo.com']

    def clean_email(self):
        """
        Validate that the email is unique in the database and that it is not
        part of a free email provider.
        
        """
        
        if User.objects\
            .filter(email__iexact=self.cleaned_data['email']):
        
            raise forms\
                .ValidationError(_("This email address is already in "
                                   "use. Please provide a different "
                                   "email address."))
        
        if self.check_domains:
        
            email_domain = self.cleaned_data['email'].split('@')[1]
            
            if email_domain in self.bad_domains:
                raise forms.ValidationError(_("Registration using free email \
                                                addresses is prohibited. \
                                                Please supply a different \
                                                email address."))
      
        return self.cleaned_data['email']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password' in self.cleaned_data \
            and 'password_c' in self.cleaned_data:
            
            if self.cleaned_data['password'] != \
                self.cleaned_data['password_c']:
                
                raise forms.ValidationError(_("The two password fields didn't \
                                                match."))

        return self.cleaned_data


class RegistrationForm(BaseUserProfileForm):
    """
    This class extracts all information from the database, related to a given 
    user and its linked UserProfile.
    """ 

    username = forms.CharField(label=_("Username"))    
    password_c = PasswordField(label=_("Confirm password"))

    class Meta:
        """Model to be used from within this form."""
    
        model = UserProfile
        fields = ('username', 'first_name', 'last_name', 'email',
                  'organization', 'country', 'password')
        widgets = {'password': forms.PasswordInput()}


class EditProfileForm(BaseUserProfileForm):
    """
    This class extracts only a few of all of the data fields that define the
    profile from a given user. Its objective is to show only the information
    that the user can edit from the associated view.
    """
    
    username = forms.CharField(label=_("Username"))

    class Meta:
        """Model to be used from within this form."""

        model = UserProfile
        fields = ('username', 'first_name', 'last_name',
                  'organization', 'country')
