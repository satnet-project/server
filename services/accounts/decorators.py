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

from django.contrib.auth.decorators import login_required as \
    auth_login_required
from website import settings as satnet_settings


def login_required(view_func):
    """Activable decorator overriding login_required
    Decorator that activates the login authentication process depending on
    whether the configuration for the application requires it or not. This
    allows testing without the necessity of login continuously into the
    application. This behavior can be changed by changing the
    JRPC_LOGIN_REQUIRED flag that can be found in the settings.py file.

    :param view_func: Django view function
    :return: View function wrapped by login_required if so configured
    """

    if satnet_settings.JRPC_LOGIN_REQUIRED:
        return auth_login_required(view_func)
    else:
        return view_func
