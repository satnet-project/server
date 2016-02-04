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
import logging

from django.db import models
from django.contrib.auth import models as auth_models
from django.shortcuts import get_object_or_404
from django_countries.fields import CountryField

from services.accounts import utils as account_utils
from website import settings as satnet_settings

logger = logging.getLogger('accounts')


class UserProfileManager(models.Manager):
    """
    Custom manager that implements a set of function to perform basic tasks
    over the users and profiles of this extended model.
    """

    def create_anonymous(self):
        """Create manager method
        Creates a profile for an anonymous user.
        :return: Reference to the just-created profile
        """
        profile = self.create(
            username=account_utils.generate_random_username(),
            first_name='Anonymous',
            last_name='User',
            is_active=True,
            anonymous=True,
            country='US',
            organization='SATNET'
        )
        profile.set_unusable_password()
        profile.save()

        return profile

    # noinspection PyMethodMayBeStatic
    def verify_user(self, user_id):
        """
        Function that changes user status to 'verified' in the database.
        
        :parameter user_id:
            Identifier of the user
        :type user_id:
            int
        :returns:
            None
        """
        user = get_object_or_404(UserProfile, user_ptr=user_id)
        user.is_verified = True
        user.save()

        allauth_adapter.get_adapter().send_mail(
            template_prefix='email/email_user_activated',
            email=user.email,
            context={
                'user_email': user.email,
            }
        )

    # noinspection PyMethodMayBeStatic
    def block_user(self, user_id):
        """
        Function that changes user status to 'blocked' in the database.
        
        :parameter user_id:
            Identifier of the user
        :type user_id:
            int
        :returns:
            None
        """
        user = get_object_or_404(UserProfile, user_ptr=user_id)
        user.blocked = True
        user.save()

        allauth_adapter.get_adapter().send_mail(
            template_prefix='email/email_user_blocked',
            email=user.email,
            context={
                'user_email': user.email,
            }
        )

    # noinspection PyMethodMayBeStatic
    def unblock_user(self, user_id):
        """
        Function that changes user status to 'unblocked' in the database.
        
        :parameter user_id:
            Identifier of the user
        :type user_id:
            int
        :returns:
            None
        """
        user = get_object_or_404(UserProfile, user_ptr=user_id)
        user.blocked = False
        user.save()

        allauth_adapter.get_adapter().send_mail(
            template_prefix='email/email_user_activated',
            email=user.email,
            context={
                'user_email': user.email,
            }
        )

    # noinspection PyMethodMayBeStatic
    def activate_user(self, user_id):
        """
        Function that changes user status to 'active' in the database.
        
        :parameter user_id:
            Identifier of the user
        :type user_id:
            int
        :returns:
            None
        """
        user = get_object_or_404(UserProfile, user_ptr=user_id)
        user.is_active = True
        user.save()

        allauth_adapter.get_adapter().send_mail(
            template_prefix='email/email_user_activated',
            email=user.email,
            context={
                'user_email': user.email,
            }
        )

    # noinspection PyMethodMayBeStatic
    def deactivate_user(self, user_id):
        """
        Function that changes user status to 'active' in the database.
        
        :parameter user_id:
            Identifier of the user
        :type user_id:
            int
        :returns:
            None
        """
        user = get_object_or_404(UserProfile, user_ptr=user_id)
        user.is_active = False
        user.save()

        allauth_adapter.get_adapter().send_mail(
            template_prefix='email/email_user_blocked',
            email=user.email,
            context={
                'user_email': user.email,
            }
        )


# noinspection PyAbstractClass
class UserProfile(auth_models.User):
    """
    This class holds additional data required from each user. It is used in 
    accordance with the process for extending the User model from 
    django.contrib.auth, in accordance with Django's website.
    """
    objects = UserProfileManager()

    organization = models.CharField(
        'Name of the organization that the user belongs to',
        max_length=100
    )
    # Country of origin of the organization that the user belongs to.
    country = CountryField()

    is_verified = models.BooleanField(
        'Flag that sets this user profile as verified',
        default=False
    )
    blocked = models.BooleanField(
        'Flat that sets this user profile as blocked',
        default=False
    )
    anonymous = models.BooleanField(
        'Flag that sets this user as an anonymous user',
        default=False
    )


# noinspection PyUnusedLocal
def create_admin_profile(apps, schema_editor):
    """Data migrations
    This method creates the profile for the initial administrator user added
    by default by django manage.py.

    :param apps: Not used variable
    :param schema_editor: Not used variable
    """
    UserProfile.objects.create(
        user_ptr=auth_models.User.objects.get(is_superuser=True),
        organization='The SATNet Network',
        country='US'
    )


# noinspection PyUnusedLocal
def remove_admin_profile(apps, schema_editor):
    """Data migrations
    Reverse data migration that destroys the user profile initially created
    for the administrator.

    :param apps: Not used variable
    :param schema_editor: Not used variable
    """
    UserProfile.objects.get(pk=1).delete()


PERMISSION_EX_MSG = 'No HTTP request: using testing identity.'


def get_user(
    http_request=None,
    permissions_flag=satnet_settings.JRPC_PERMISSIONS,
    test_username=satnet_settings.TEST_USERNAME,
    testing_flag=satnet_settings.TESTING
):
    """
    Returns the username of the user within a given HTTP request object. It
    takes into account all the permission policies implemented by the server.

    #### TODO # For some reason, the user object returned is a
    <SimpleLazyObject> that cannot be directly assigned as the owner of any
    segment and, within the create method for Spacecraft and Ground Station,
    they duplicate half the functionality of this method here.

    :param http_request: The HTTP request object
    :param permissions_flag: Flag with whether the permissions should be used
    :param test_username: Flag with the test username
    :param testing_flag: Flag indicating the testing condition
    :return: (user, username) Tuple with the user object as per django_auth
        contrib library and its username separate
    """
    if not permissions_flag and not testing_flag:

        logger.warn(PERMISSION_EX_MSG)
        username = test_username
        user = UserProfile.objects.get(username=username)

        if user is None:
            raise Exception('User <' + username + '> could not be found.')

    else:

        user = http_request.user
        username = user.username

    return user, username
