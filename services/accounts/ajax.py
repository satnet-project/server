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

from services.accounts import decorators as account_decorators
from django.contrib.auth import models as auth_models
from django.contrib.sites import models as site_models
from django.forms import models as form_models
from django.shortcuts import get_object_or_404

import logging
import json
from jsonview import decorators, exceptions

from services.accounts import models, utils

logger = logging.getLogger('accounts')


@decorators.json_view
@account_decorators.login_required
def user_details(request):
    """jQuery GET method for retrieving user details.
    :param request: The HTTP request to be processed
    """
    logger.info(__name__ + ', user_details (AJAX)')

    if 'user_id' not in request.GET:
        raise exceptions.BadRequest("'user_id' not found as a GET parameter.")

    user_id = request.GET['user_id']

    logger.info(__name__ + ', user_id = ' + user_id)
    
    user = get_object_or_404(models.UserProfile, pk=user_id)
    fields = ['username', 'first_name', 'last_name', 'organization', 'email']
    user_dict = form_models.model_to_dict(user, fields)
    user_dict['country'] = str(user.country.name)
    
    return user_dict


@decorators.json_view
@account_decorators.login_required
def user_verification(request):
    """ jQuery POST method for updating the set of users to be verified.
    :param request: The HTTP request to be processed
    """
    logger.info(__name__ + ', user_verification (AJAX)')
    for x in request.POST:
        print((x, ':', request.POST[x]))

    if 'user_list' not in request.POST:
        print((__name__ + ', user_verification, raising BadRequest.'))
        raise Exception("'user_list' not found as a POST parameter.")

    value = str(request.POST['user_list'])
    user_list = json.loads(value)

    # noinspection PyProtectedMember
    if site_models.Site._meta.installed:
        # noinspection PyUnusedLocal
        site = site_models.Site.objects.get_current()
    else:
        # noinspection PyUnusedLocal
        site = site_models.RequestSite(request)

    v_users = []

    for user_id in user_list:
    
        # 1) first, the confirmation email is sent
        utils.allauth_confirm_email(
            auth_models.User.objects.get(pk=user_id), request
        )
        # 2) afterwards, the profile is set as verified and saved
        u_profile = get_object_or_404(models.UserProfile, pk=user_id)
        # ### Uncomment when ready ### u_profile.is_verified = True
        u_profile.save()
        # 3) this user_id is added to the list of verified ids to be returned
        v_users.append(user_id)

    j_v_users = json.dumps(v_users)
    result = dict(user_list=j_v_users)
    print((__name__ + ', user_verification, j_v_users = ' + j_v_users))

    return result
