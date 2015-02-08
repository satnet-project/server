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

from allauth.account import adapter as allauth_adapter
from allauth.account import signals as allauth_signals
from django import dispatch as django_dispatch
from django.contrib.auth import models as auth_models
from django.core import exceptions
from django.db.models import signals as django_signals
import logging
from services.accounts import models as account_models
from user_sessions import models as user_session_models

logger = logging.getLogger('accounts')


@django_dispatch.receiver(
    django_signals.post_save,
    sender=auth_models.User
)
def user_migrated(sender, instance, created, raw, **kwargs):
    """Data Migration
    Creates the user profile for the added superuser.
    :param sender: Reference to the sender.
    :param instance: Reference to object
    :param created: Flag that indicates that this object has just been created
    :param raw: Flag that indicates whether the database is stable or not
    :param kwargs: Additional arguments.
    """
    if not created or raw:
        return

    if instance.pk != 1:
        return

    account_models.create_admin_profile(None, None)


@django_dispatch.receiver(
    django_signals.pre_delete, sender=user_session_models.Session
)
def session_closed_handler(sender, instance, **kwargs):
    """Session closed signal handler
    This handler checks whether the session was owned by an anonymous user or
    not. In case the owner of the session was anonymous, it removes the
    resources allocated for that user as well.
    :param sender: Session object that sent this signal
    :param instance: Instance of the session object
    :param kwargs: Additional parameters
    """
    # ### TODO erase anonymous user as session ends!
    pass


@django_dispatch.receiver(allauth_signals.user_signed_up)
def user_signed_up_receiver(request, user, **kwargs):
    """User signed up callback
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


CONFIRMED_EMAIL_TEMPLATE = 'email/email_user_confirmed'


@django_dispatch.receiver(allauth_signals.email_confirmed)
def email_confirmed_receiver(email_address, **kwargs):
    """Email confirmed callback.
    This method overrides the default behavior for handling the sign up of a
    new user. In this case, a welcome email will be sent waiting for the
    operator of the system to accept the request made by this user.
    :param request: the signed up request
    :param user: the new user
    :param kwargs: other args
    """

    try:

        # User has to be activated by server's administrator, unless the user
        # is the administrator itself!
        user = auth_models.User.objects.get(email=email_address.email)
        if user.is_staff or user.is_superuser:
            user.is_active = True
        else:
            user.is_active = False
        user.save()

        # The confirmation of the email only verifies the account.
        u_profile = account_models.UserProfile.objects.get(
            email=email_address.email
        )
        u_profile.is_verified = True
        u_profile.save()

        # Email sent to the administrator to report the new user
        for staff_email_i in auth_models.User.objects.filter(
                is_staff=True
        ).values_list('email', flat=True):

            logger.info(
                '(((((email_confirmed))))), notifying to staff = ' + str(
                    staff_email_i
                )
            )

            allauth_adapter.get_adapter().send_mail(
                template_prefix=CONFIRMED_EMAIL_TEMPLATE,
                email=staff_email_i,
                context={
                    'staff_email': staff_email_i,
                }
            )

    except exceptions.ObjectDoesNotExist:

        logger.warning(
            'Confirmed email = <' + str(
                email_address
            ) + '> does not exist in the database.'
        )