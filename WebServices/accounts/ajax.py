import logging
logger = logging.getLogger(__name__)

import json

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

from accounts.models import UserProfile
from registration.models import RegistrationProfile

# ### FIXME Problem while raising BadRequest exception
# meanwhile, it is encouraged to utilize the less-supported django-jsonresponse
# library, with '@to_json('api')' decorator and simple 'Exception' raising
# ### jsonview / jsonresponse libraries compatibility:
# @to_json('plain') = @json_view
# @to_json('api') involves a response structure with data and error fields.
#    (*) data field is the json representation of the response
#    (*) error field is the error identifier
# ###
from jsonview.decorators import json_view
from jsonview.exceptions import BadRequest
#from jsonresponse import to_json

#@to_json('api')
@json_view
@login_required
def user_details(request):
    """
    jQuery GET method for retrieving user details. Syntax:
    
    >>> user_details(user_id)
    
    * user_id = identifier of the user within the database
    
    """

    logger.info(__name__ + ', user_details (AJAX)')

    if not 'user_id' in request.GET:
        raise BadRequest("'user_id' not found as a GET parameter.")

    user_id = request.GET['user_id']

    logger.info(__name__ + ', user_id = ' + user_id)
    
    user = get_object_or_404(UserProfile, pk=user_id)
    fields = ['username', 'first_name', 'last_name', 'organization', 'email']
    user_dict = model_to_dict(user, fields)
    user_dict['country'] = unicode(user.country.name)
    
    return user_dict

@json_view
@login_required
def user_verification(request):
    """
    jQuery POST method for updating the set of users to be verified. Syntax:
    
    >>> user_verification(user_list)
    
    * list = list with the identifiers of the verified users.
    
    """

    logger.info(__name__ + ', user_verification (AJAX)')
    logger.info(__name__ + ', user_verification, request.POST >>>>>>>> ')
    for x in request.POST:
        print (x, ':', request.POST[x])
    logger.info(__name__ + ', user_verification, request.POST <<<<<<<< ')

    if not request.POST.has_key('user_list'):
        print (__name__ + ', user_verification, raising BadRequest.')
        raise Exception("'user_list' not found as a POST parameter.")

    value = unicode(request.POST['user_list'])
    user_list = json.loads(value)

    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)

    v_users = []

    for user_id in user_list:
    
        # 1) first, the confirmation email is sent
        r_profile = get_object_or_404(RegistrationProfile, user_id=user_id)
        r_profile.send_activation_email(site)
        # 2) afterwards, the profile is set as verified and saved
        u_profile = get_object_or_404(UserProfile, pk=user_id)
        # ### Uncomment when ready ### u_profile.is_verified = True
        u_profile.save()
        # 3) this user_id is added to the list of verified ids to be returned
        v_users.append(user_id)

    j_v_users = json.dumps(v_users)
    result = dict(user_list = j_v_users)
    print (__name__ + ', user_verification, j_v_users = ' + j_v_users)

    return result

