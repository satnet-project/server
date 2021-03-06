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

from django.template import response as django_response
from services.accounts import backend as accounts_backend


def redirect_operations(request):
    """Redirect method
    Redirects users either to their C2 interface or to the login window.

    :param request: HTTP request
    """
    return django_response.TemplateResponse(
        request, 'angular/users_operations.html'
    )


def redirect_leop(request, identifier):
    """Redirect method
    Redirects staff either to the LEOP interface or to the login page.

    :param request: HTTP request
    :param identifier: Identifier for the LEOP
    """
    user_profile = accounts_backend.authenticate_anonymous(request)
    return django_response.TemplateResponse(
        request, 'angular/staff_leop.html',
        {
            'leop_id': identifier,
            'is_anonymous': user_profile.anonymous
        }
    )
