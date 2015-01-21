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

######## Anonymous authentication backend middleware #########

from django.contrib import auth as django_auth
from django.contrib.auth import models as auth_models
import random

_MAX_INT_ANONYMOUS = 10000


def authenticate_anonymous(request):
    # do we have an existing user?
    if request.user.is_authenticated():
        return request.user
    else:
        # if not, create an anonymous user and log them in
        username = 'anonymous' + str(random.randint(0, _MAX_INT_ANONYMOUS))
        user = auth_models.User(
            username=username, first_name='Anonymous', last_name='User'
        )
        user.set_unusable_password()
        user.save()
        user.username = user.id
        user.save()

        # comment out the next two lines if you aren't using profiles
        #p = account_models.UserProfile(user=u, anonymous=True)
        #p.save()
        django_auth.authenticate(user=user)
        django_auth.login(request, user)
        return user


class AnonymousAuthenticationBackend(object):
    """
    This is for automatically signing in the user after signup etc.
    """

    def authenticate(self, user=None):
        # make sure they have a profile and that they are anonymous
        # if you're not using profiles you can just return user
        # if not user.get_profile() or not user.get_profile().anonymous:
        #    user = None
        return user

    def get_user(self, user_id):
        try:
            return auth_models.User.objects.get(pk=user_id)
        except auth_models.User.DoesNotExist:
            return None