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

from allauth.account import utils as allauth_utils, models as allauth_models
from django import forms
from django.utils.translation import ugettext_lazy as _
import logging
import re
import random

logger = logging.getLogger(__name__)

p = re.compile('^op_([0-9]+)$')
p_id = re.compile('([0-9]+)')


def get_user_operations(request):
    """
    This function returns a dictionary with the set of operations (as values) 
    to be carried out over each user (as keys). Only a single operation is 
    permitted over a single user.
    
    :param request:
        The data input from the page's form
    :type request:
        Dictionary (Python Framework)
    :returns:
        A dictionary with the operations found
    :rtype:
        Dictionary (Python Framework)
    
    :Author:
        Ricardo Tubio-Pardavila (rtubiopa@calpoly.edu)
    """
    operations = {}

    for k, operation in request.iteritems():
        
        if not p.match(k):
            continue
        
        ids = p_id.findall(k)

        if len(ids) != 1:
            continue
        
        user_id = ids.pop() 
        operations[user_id] = operation

    return operations


# To change the list of banned domains, subclass this form and
# override the attribute ``bad_domains``.
forbidden_domains = [
    'aim.com', 'aol.com', 'email.com', 'gmail.com', 'googlemail.com',
    'hotmail.com', 'hushmail.com', 'msn.com', 'mail.ru', 'mailinator.com',
    'live.com', 'yahoo.com'
]


def validate_email(email):
    """Checks mail address validity.
    This method is used for checking whether a given email address is
    valid or not (free mail providers are forbidden).
    :param email: email address to be checked
    :return: 'True' in case the email address is valid
    :raises ValidationError: in case the email is not valid
    """
    email_domain = email.split('@')[1]

    if email_domain in forbidden_domains:

        raise forms.ValidationError(
            _(
                "Registration using free email addresses is forbidden. Please"
                "provide a different email address."
            )
        )

    return True


def allauth_confirm_email(user, request):
    """django-allauth confirmation email.
    This method sends a confirmation email to the given user.
    :param user: the user whose confirmation is still missed
    :param request: the request object for the view that requests this
    confirmation
    """
    email = allauth_utils.user_email(user)
    email_address = allauth_models.EmailAddress.objects.get_for_user(
        user, email
    )
    email_address.send_confirmation(request, signup=True)


MAX_INT_ANONYMOUS = 9999999


def generate_random_username():
    """Generate function
    Generates a random username for anonymous users.
    :returns: String with the anonymous username
    """
    random.seed()
    return 'anon-' + str(random.randint(0, MAX_INT_ANONYMOUS))