"""
   Copyright [yyyy] [name of copyright owner]

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

import account.views

from WebServices.forms import SignupForm
from WebServices.models import Account

"""
Class that extends <SignupView> from django-user-accounts in order to provide a
personalized UserProfile with which get some more data from system users.
"""
class SignupView(account.views.SignupView):

    """This is the form that it is enclosed."""
    form_class = SignupForm
    
    """Constructor"""
    def __init__(self, *args, **kwargs):
        self.created_user = None
        kwargs["signup_code"] = None
        super(SignupView, self).__init__(*args, **kwargs)
        
    """
    Overriden method. Creates an Account object that, in this case, has 
    extended the original Account class from django-user-accounts.
    
    self -- ()
    form -- reference to the form enclosed
    """
    def create_account(self, form):
        return Account.create\
            (request=self.request, user=self.created_user, create_email=False)

