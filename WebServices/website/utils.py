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

import traceback

from django.contrib.auth import models as auth_models
from django.core import exceptions

_ADMIN_DEFAULT_CFG = {
    'username': 'satnet_admin',
    'password': 'satnet805calpoly',
    'email': 'satnet.calpoly@gmail.com'
}


def test_create_admin(sender, **kwargs):
    """Creates an admin user.
    This function should be invoked as a callback to signals.post_syncdb.
    """
    try:

        auth_models.User.objects.get(username=_ADMIN_DEFAULT_CFG['username'])
        return

    except exceptions.ObjectDoesNotExist:

        auth_models.User.objects.create_superuser(
            _ADMIN_DEFAULT_CFG['username'],
            _ADMIN_DEFAULT_CFG['email'],
            _ADMIN_DEFAULT_CFG['password']
        )


def get_traceback_as_str():
    """
    This method simply returns a string that contains the frames of the current
    traceback stack.
    """
    return ''.join(str(e) for e in traceback.format_stack())