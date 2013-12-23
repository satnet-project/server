import logging
logger = logging.getLogger(__name__)

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from registration import signals
from registration.models import RegistrationProfile
from registration.backends.default.views import RegistrationView

from accounts.forms import RegistrationForm, EditProfileForm
from accounts.helpers import get_user_operations
from accounts.models import UserProfile, UserProfileManager

from smtplib import SMTPSenderRefused

class UserProfileView(UpdateView):
    """
    This class shows a view for users to edit the details of their profiles.
    
    :Author:
        Ricardo Tubio-Pardavila (rtubiopa@calpoly.edu)
    """
    
    """HTML template to be used"""
    model = UserProfile
    form_class = EditProfileForm
    template_name = 'users/user_profile_form.html'
    success_url = '/accounts/login_ok/'
    
    def get_object(self, queryset=None):
        return UserProfile.objects.get(pk=self.request.user.id)

class RegisterView(RegistrationView):
    """
    This is a form that contains all the required fields from the UserProfile 
    and User tables, as selected by the constructor of the form_class class.
    """

    """HTML template to be used"""
    template_name = 'registration/registration_form.html'
    success_url = '/'
    form_class = RegistrationForm 

    def register(self, request, **cleaned_data):
        """
        This method overrides the register method of the selected backend. It
        implements all the same operations than the original one, with the
        exception that it does not send the confirmation email to the user. 
        This way, it permits an intermediate step in which the network 
        administrator first accepts the registration request.
        """
        
        username, email, password = cleaned_data['username'], \
                                    cleaned_data['email'], \
                                    cleaned_data['password']

        first_name, last_name = cleaned_data['first_name'], \
                                cleaned_data['last_name']

        organization, country = cleaned_data['organization'], \
                                cleaned_data['country']

        user_profile = UserProfile.objects\
                            .create(username=username,\
                                    first_name=first_name,\
                                    last_name=last_name,\
                                    email=email,\
                                    organization=organization,\
                                    country=country,\
                                    is_active=False,\
                                    is_verified=False)
        
        user_id = user_profile.user_ptr_id
        new_user = User.objects.get(id=user_id)
        new_user.set_password(password)
        new_user.save()
        
        registration_profile = RegistrationProfile.objects\
                                                    .create_profile(new_user)
        
        signals.user_registered.send(sender=self.__class__, \
                                     user=new_user, \
                                     request=request, \
                                     cleaned_data=cleaned_data, \
                                     registration_profile=registration_profile)
                                     
        return user_profile

class PendingRegView(ListView):
    """
    This class helps in handling how users are shown to the network
    administrator, so that their activation can be initiated. This is the
    second step of the registration process, that takes place after a user has
    sent the registration request.
    """
    
    model = UserProfile
    template_name = 'staff/registration_requests.html'
    queryset = UserProfile.objects.filter(is_verified=False)\
                                    .filter(is_blocked=False)
    context_object_name = "user_list"

    def post(self, request, *args, **kwargs):
        """
        POST method handler. This method is invoked once the submit button of 
        the form is pressed.

        """
        
        # 1) from the request, get all username tags with operations pending
        operations = get_user_operations(request.POST)
                
        # 2) apply, one-by-one, batched operations
        self.apply_user_operations(operations)
 
        # after all operations had been carried out, the same page (but updated
        # is returned
        return self.get(request, *args, **kwargs)

    def apply_user_operations(self, operations):
        """
        Applies all the batched operations over the given users and saves the
        changes in all the correspondent database tables. This is a generic
        method whose supported operations are defined in a dictionary that 
        links the key (operation name) with the callback function that
        implements that operation. Therefore, this class can be extended and,
        by simply modifying that dictionary, new operations can be implemented.
        
        :param operations:
            Dictionary whose keys are the identifiers for the users and whose
            values are the operations to be applied to each user
        :type operations:
            Dictionary
        :returns None:
            None
            
        """
    
        for user_id, op in operations.iteritems():

            logger.debug(__name__ + ', op = ' + op + ', on user = ' + user_id)

            try:
                self.operations[str(op)](self, user_id)
            except KeyError:
                logger.exception(__name__ + ', op = ' + op + ' not found.')

    def activate_user(self, user_id):
        """
        Activates a given user in the database and triggers the automatic
        sending of the account verification email.
        
        :parameter user_id:
            Identifier of the user
        :type user_id:
            int
        :returns:
            None
            
        """
    
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        # 1) first, the confirmation email is sent
        r_profile = get_object_or_404(RegistrationProfile, user_id=user_id)
        try:
            r_profile.send_activation_email(site)
        except SMTPSenderRefused, e:
            logger.exception(e)
            
        # 2) afterwards, the profile is set as verified and saved
        UserProfile.objects.verify_user(user_id)
   
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
        
        UserProfile.objects.block_user(user_id)

    def delete_user(self, user_id):
        """
        Deletes all the information related to a given user from the 3 tables
        where information is stored: User (django.contrib.auth), 
        UserProfile (accounts) and RegistrationProfile (django-registration).
        
        :parameter user_id:
            Identifier of the user
        :type user_id:
            int
        :returns:
            None
            
        """

        logger.debug(__name__ + ', delete_user = ' + user_id)
        
        try:
            
            u_profile = UserProfile.objects.get(pk=user_id)
            u_profile.delete()
            return
        
        except ObjectDoesNotExist:
            logger.exception(__name__ + ', deleting UserProfile(' \
                                        + user_id + ')')
        
        try:
            
            r_profile = RegistrationProfile.objects.get(user_id=user_id)
            r_profile.delete()
            return
        
        except ObjectDoesNotExist:
            logger.exception(__name__ + ', deleting RegistrationProfile(' \
                                        + user_id + ')')

    # Operations dictionary
    operations = {
        'verify' : activate_user,
        'block'  : block_user,
        'delete' : delete_user,
    }
        
class BlockedRegView(PendingRegView):
    """
    This class helps in showing a list of blocked users to the network 
    administrator.
    
    :Author:
        Ricardo Tubio-Pardavila (rtubiopa@calpoly.edu)
    
    """
    
    template_name = 'staff/blocked_requests.html'
    queryset = UserProfile.objects.filter(is_blocked=True)

    def unblock_user(self, user_id):
        """
        Unblocks a registration request made by the user whose identifier is
        the given parameter.
        
        :parameter user_id:
            Identifier of the user
        :type user_id:
            int
        :returns:
            None
            
        """
        
        UserProfile.objects.unblock_user(user_id)
    
    operations = {
        'unblock' : unblock_user,
        'delete'  : PendingRegView.delete_user,
    }

class VerifiedView(PendingRegView):
    """
    View of the already registered users within the network.
    
    :Author:
        Ricardo Tubio-Pardavila (rtubiopa@calpoly.edu)
    
    """

    template_name = 'staff/verified_requests.html'
    queryset = UserProfile.objects.filter(is_active=True) \
                                    .filter(is_verified=True) \
                                    .filter(is_blocked=False)

    def deactivate_user(self, user_id):
        """
        Marks the given user as inactive, so that the user cannot login in
        the system.
        
        :parameter user_id:
            Identifier of the user
        :type user_id:
            int
        :returns:
            None
            
        """
        
        UserProfile.objects.deactivate_user(user_id)

    operations = {
        'deactivate' : deactivate_user,
        'delete'     : PendingRegView.delete_user,
    }
    
class InactiveView(PendingRegView):
    """
    View of the inactive users within the network.
    
    :Author:
        Ricardo Tubio-Pardavila (rtubiopa@calpoly.edu)
    
    """

    template_name = 'staff/inactive_users.html'
    queryset = UserProfile.objects.filter(is_active=False) \
                                    .filter(is_verified=True) \
                                    .filter(is_blocked=False)
    
    def activate_user(self, user_id):
        """
        Marks the given user as active, so that the user cannot login in the 
        system.
        
        :parameter user_id:
            Identifier of the user
        :type user_id:
            int
        :returns:
            None
            
        """
        
        UserProfile.objects.activate_user(user_id)
        
    operations = {
        'activate' : activate_user,
        'delete'   : PendingRegView.delete_user,
    }
    
################################################################################
# ### Standalone view handlers
################################################################################

def csrf_failure_handler(request, reason=""):
    """
    Method that renders the HTML to be displayed whenever a CSRF exception is
    raised.
    
    """

    return TemplateResponse(request, "registration/csrf_failure.html")

def redirect_home(request):
    """
    Redirects user access to 'home', so in case a user is already logged in,
    the system redirects that access to the post-login 'home' page.
    
    """

    logger.info('>>>>>> redirect_home, is_staff? ' \
                                    + str(request.user.is_staff))
    
    if request.user.is_authenticated():
        return redirect_login(request)
    else:
        return TemplateResponse(request, 'index.html')

@login_required
def redirect_login(request):
    """
    Redirects users based on their priviledges.
    
    """
    
    logger.info('>>>>>> redirect_login, is_staff? ' \
                                    + str(request.user.is_staff))
    
    if request.user.is_staff:
        return TemplateResponse(request, "staff/staff_home.html")
    else:
        return TemplateResponse(request, "users/users_home.html")

