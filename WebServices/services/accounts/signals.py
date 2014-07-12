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

from django.contrib.auth import models as auth_models
from django.core import exceptions

from allauth.account import models, signals
import logging

logger = logging.getLogger('accounts')


def user_signed_up_receiver(request, user, **kwargs):
    """User signed up callback.
    This method overrides the default behavior for handling the sign up of a
    new user. In this case, a welcome email will be sent waiting for the
    operator of the system to accept the request made by this user.
    :param request: the signed up request
    :param user: the new user
    :param kwargs: other args
    """
    logger.info(
        '((((((user_signed_up)))))), user = ' + str(user)
    )


def email_confirmed_receiver(email_address, **kwargs):
    """Email confirmed callback.
    This method overrides the default behavior for handling the sign up of a
    new user. In this case, a welcome email will be sent waiting for the
    operator of the system to accept the request made by this user.
    :param request: the signed up request
    :param user: the new user
    :param kwargs: other args
    """
    logger.info(
        '((((((email_confirmed)))))), email = ' + str(email_address.email)
    )

    try:

        user = auth_models.User.objects.get(email=email_address.email)
        user.is_active = True
        user.save()

    except exceptions.ObjectDoesNotExist:

        logger.warning(
            'Confirmed email = <' + str(email_address) + '> does not exist in'
            'the database.'
        )


def connect_user_2_accounts():
    """Callbacks connection function.
    Simple function that connects the callbacks from the allauth signals to
    the receiver for the accounts application.
    """
    signals.user_signed_up.connect(
        user_signed_up_receiver,
    )
    signals.email_confirmed.connect(
        email_confirmed_receiver,
        sender=models.EmailConfirmation
    )