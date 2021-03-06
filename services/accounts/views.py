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

from django.core import exceptions
from django.core import urlresolvers
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from services.accounts import forms, models, utils

import logging
logger = logging.getLogger(__name__)


def csrf_failure_handler(request, reason=''):
    """
    Method that renders the HTML to be displayed whenever a CSRF exception is
    raised.

    :param request: HTTP request to be processed
    :param reason: String describing the reason of the CSRF failure
    """
    logger.error('CSRF ERROR, reason = ' + str(reason))
    return TemplateResponse(request, 'csrf_failure.html')


def redirect_login(request):
    """Redirect method
    Redirects user access to 'home', so in case a user is already logged in,
    the system redirects that access to the post-login 'home' page.

    :param request: HTTP request to be processed
    """
    if request.user.is_authenticated():
        return redirect_home(request)
    else:
        return TemplateResponse(request, 'index.html')


@login_required
def redirect_home(request):
    """Redirect method
    Redirects users based on their priviledges.

    :param request: HTTP request to be processed
    """
    if request.user.is_staff:
        return TemplateResponse(request, 'staff/staff_home.html')
    else:
        return TemplateResponse(request, 'users/users_home.html')


class UserProfileView(UpdateView):
    """
    This class shows a view for users to edit the details of their profiles.
    """
    model = models.UserProfile
    form_class = forms.ProfileUpdateForm
    template_name = 'users/user_profile_form.html'
    success_url = urlresolvers.reverse_lazy(redirect_home)

    def get_context_data(self, **kwargs):
        """ Returns the context data dictionary for the template (overriden).
        For this view it is necessary to change dinamically the base template
        that this template extends since it is different depending on whether
        the user is a regular or a staff one.
        :param kwargs: Additional parameters
        """
        context = super(UserProfileView, self).get_context_data(**kwargs)

        # noinspection PyUnresolvedReferences
        if self.request.user.is_authenticated():

            # noinspection PyUnresolvedReferences
            context['username'] = self.request.user.username

            # noinspection PyUnresolvedReferences
            if self.request.user.is_staff:
                context['base_template'] = 'staff/staff_home.html'
            else:
                context['base_template'] = 'users/users_home.html'

        else:
            raise exceptions.PermissionDenied(_("User is not authenticated."))

        return context

    def get_object(self, queryset=None):
        """Overriden <get_object>.
        This method is overriden so that it returns a UserProfile both for
        regular and for staff users.

        :param queryset: Query set parameter for looking up for the object
        :return: UserProfile object to be shown
        """

        # noinspection PyUnresolvedReferences
        if self.request.user.is_authenticated():
            # noinspection PyUnresolvedReferences
            return models.UserProfile.objects.get(pk=self.request.user.id)


class PendingRegView(ListView):
    """
    This class helps in handling how users are shown to the network
    administrator, so that their activation can be initiated. This is the
    second step of the registration process, that takes place after a user has
    sent the registration request.
    """
    model = models.UserProfile
    template_name = 'staff/registration_requests.html'
    queryset = models.UserProfile.objects.\
        filter(is_verified=False).\
        filter(blocked=False)
    context_object_name = 'user_list'

    def post(self, request, *args, **kwargs):
        """POST method handler

        This method is invoked once the submit button of the form is pressed.

        :param request: HTTP request to be processed
        :param args: Additional parameters list
        :param kwargs: Additional parameters dictionary
        """
        operations = utils.get_user_operations(request.POST)
        self.apply_user_operations(operations)
        return self.get(request, *args, **kwargs)

    def apply_user_operations(self, operations):
        """
        Applies all the batched operations over the given users and saves the
        changes in all the correspondent database tables. This is a generic
        method whose supported operations are defined in a dictionary that
        links the key (operation name) with the callback function that
        implements that operation. Therefore, this class can be extended and,
        by simply modifying that dictionary, new operations can be implemented.

        :param operations: Dictionary whose keys are the identifiers for the
            users and whose values are the operations to be applied to each
            user
        """
        for user_id, op in operations.items():

            logger.debug(__name__ + ', op = ' + op + ', on user = ' + user_id)

            try:
                op_function = self.operations[str(op)]
                op_function(self, user_id)
            except KeyError:
                logger.exception(__name__ + ', op = ' + op + ' not found.')

    def activate_user(self, user_id):
        """
        Activates a given user in the database.
        :parameter user_id: Identifier of the user
        :type user_id: int
        """
        models.UserProfile.objects.verify_user(user_id)

    # noinspection PyMethodMayBeStatic
    def block_user(self, user_id):
        """
        Blocks a registration request made by the user whose identifier is
        the given parameter.

        :parameter user_id:
            Identifier of the user
        :type user_id:
            int
        :returns:
            None

        """
        models.UserProfile.objects.block_user(user_id)

    # noinspection PyMethodMayBeStatic
    def delete_user(self, user_id):
        """
        Deletes all the information related to a given user from the 3 tables
        where information is stored: User (django.contrib.auth),
        UserProfile (accounts) and RegistrationProfile (django-registration).
        :parameter user_id:
            Identifier of the user
        """
        logger.debug(__name__ + ', delete_user = ' + user_id)

        try:

            u_profile = models.UserProfile.objects.get(pk=user_id)
            u_profile.delete()
            return

        except exceptions.ObjectDoesNotExist:
            logger.exception(
                __name__ + ", deleting models.UserProfile(" + user_id + ")"
            )

    # Operations dictionary
    operations = {
        'verify': activate_user,
        'block': block_user,
        'delete': delete_user,
    }


class BlockedRegView(PendingRegView):
    """
    This class helps in showing a list of blocked users to the network
    administrator.
    """
    template_name = 'staff/blocked_requests.html'
    queryset = models.UserProfile.objects.filter(blocked=True)

    # noinspection PyMethodMayBeStatic
    def unblock_user(self, user_id):
        """
        Unblocks a registration request made by the user whose identifier is
        the given parameter.
        :parameter user_id: Identifier of the user
        """
        models.UserProfile.objects.unblock_user(user_id)

    operations = {
        'unblock': unblock_user,
        'delete': PendingRegView.delete_user,
    }


class VerifiedView(PendingRegView):
    """
    View of the already registered users within the network.
    """
    template_name = 'staff/verified_requests.html'
    queryset = models.UserProfile.objects.\
        filter(is_active=True).\
        filter(is_verified=True).\
        filter(blocked=False)

    # noinspection PyMethodMayBeStatic
    def deactivate_user(self, user_id):
        """
        Marks the given user as inactive, so that the user cannot login in
        the system.
        :parameter user_id: Identifier of the user
        """
        models.UserProfile.objects.deactivate_user(user_id)

    operations = {
        'deactivate': deactivate_user,
        'delete': PendingRegView.delete_user,
    }


class InactiveView(PendingRegView):
    """
    View of the inactive users within the network.
    """
    template_name = 'staff/inactive_users.html'
    queryset = models.UserProfile.objects.\
        filter(is_active=False).\
        filter(is_verified=True).\
        filter(blocked=False)

    def activate_user(self, user_id):
        """
        Marks the given user as active, so that the user cannot login in the
        system.
        :parameter user_id: Identifier of the user
        """
        models.UserProfile.objects.activate_user(user_id)
        
    operations = {
        'activate': activate_user,
        'delete': PendingRegView.delete_user,
    }
