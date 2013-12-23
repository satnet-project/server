from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from accounts.ajax import user_details, user_verification
from accounts.views import redirect_home
from accounts.views import RegisterView, PendingRegView, BlockedRegView, \
                            VerifiedView, InactiveView, UserProfileView

urlpatterns = patterns('',

    url(r'^register/$', \
        RegisterView.as_view(), \
        name='register'),
    url(r'^login_ok/$', \
        redirect_home, \
        name='login_ok'),
    
    # ### Staff specific views
    url(r'^pending/$', \
        login_required(PendingRegView.as_view()), \
        name='pending'),
    url(r'^blocked/$', \
        login_required(BlockedRegView.as_view()), \
        name='blocked'),
    url(r'^verified/$', \
        login_required(VerifiedView.as_view()), \
        name='verified'),
    url(r'^inactive/$', \
        login_required(InactiveView.as_view()), \
        name='inactive'),
    
    # ### User specific views
    url(r'^user_profile/$', \
        login_required(UserProfileView.as_view()), \
        name='user_profile'),

    # ### AJAX views
    url(r'^ajax/user_details/$', \
        user_details, \
        name='ajax_user_details'),
    url(r'^ajax/user_verification/$', \
        user_verification, \
        name='ajax_user_verification'),

)

