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

from django.contrib import auth as django_auth
from django.contrib.auth import models as auth_models
from services.accounts import models as account_models


def authenticate_anonymous(request):
    # do we have an existing user?
    if request.user.is_authenticated():
        return account_models.UserProfile.objects.get(
            username=request.user.username
        )
    else:
        anonymous_u = account_models.UserProfile.objects.create_anonymous()
        django_auth.authenticate(user=anonymous_u)
        django_auth.login(request, anonymous_u)
        return anonymous_u


class AnonymousAuthenticationBackend(object):
    """
    This is for automatically signing in the user after signup etc.
    """

    # noinspection PyMethodMayBeStatic
    def authenticate(self, user=None):
        """
        Authenticates the given user.
        :param user: User object to be authenticated
        :return: The same user object
        """
        return user

    # noinspection PyMethodMayBeStatic
    def get_user(self, user_id):
        """
        Returns the user object related with the given user_id.
        :param user_id: Identifier of the user object
        :return: Reference to the User object (or none if it does not exist)
        """
        try:
            return auth_models.User.objects.get(pk=user_id)
        except auth_models.User.DoesNotExist:
            return None
