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

import logging
from django.db import models
from django.contrib.auth import models as auth_models
from django.shortcuts import get_object_or_404
from django_countries.fields import CountryField
from django.contrib.sessions.models import Session

from allauth.account import adapter as allauth_adapter

logger = logging.getLogger('accounts')


class UserProfileManager(models.Manager):
    """
    Custom manager that implements a set of function to perform basic tasks
    over the users and profiles of this extended model.
    """
    def verify_user(self, user_id):
        """
        Function that changes user status to 'verified' in the database.
        
        :parameter user_id:
            Identifier of the user
        :type user_id:
            int
        :returns:
            None
        """
        user = get_object_or_404(UserProfile, user_ptr=user_id)
        user.is_verified = True
        user.save()

        allauth_adapter.get_adapter().send_mail(
            template_prefix='email/email_user_activated',
            email=user.email,
            context={
                'user_email': user.email,
            }
        )

    def block_user(self, user_id):
        """
        Function that changes user status to 'blocked' in the database.
        
        :parameter user_id:
            Identifier of the user
        :type user_id:
            int
        :returns:
            None
        """
        user = get_object_or_404(UserProfile, user_ptr=user_id)
        user.is_blocked = True
        user.save()

        allauth_adapter.get_adapter().send_mail(
            template_prefix='email/email_user_blocked',
            email=user.email,
            context={
                'user_email': user.email,
            }
        )

    def unblock_user(self, user_id):
        """
        Function that changes user status to 'unblocked' in the database.
        
        :parameter user_id:
            Identifier of the user
        :type user_id:
            int
        :returns:
            None
        """
        user = get_object_or_404(UserProfile, user_ptr=user_id)
        user.is_blocked = False
        user.save()

        allauth_adapter.get_adapter().send_mail(
            template_prefix='email/email_user_activated',
            email=user.email,
            context={
                'user_email': user.email,
            }
        )

    def activate_user(self, user_id):
        """
        Function that changes user status to 'active' in the database.
        
        :parameter user_id:
            Identifier of the user
        :type user_id:
            int
        :returns:
            None
        """
        user = get_object_or_404(UserProfile, user_ptr=user_id)
        user.is_active = True
        user.save()

        allauth_adapter.get_adapter().send_mail(
            template_prefix='email/email_user_activated',
            email=user.email,
            context={
                'user_email': user.email,
            }
        )

    def deactivate_user(self, user_id):
        """
        Function that changes user status to 'active' in the database.
        
        :parameter user_id:
            Identifier of the user
        :type user_id:
            int
        :returns:
            None
        """
        user = get_object_or_404(UserProfile, user_ptr=user_id)
        user.is_active = False
        user.save()

        allauth_adapter.get_adapter().send_mail(
            template_prefix='email/email_user_blocked',
            email=user.email,
            context={
                'user_email': user.email,
            }
        )


class UserProfile(auth_models.User):
    """
    This class holds additional data required from each user. It is used in 
    accordance with the process for extending the User model from 
    django.contrib.auth, in accordance with Django's website.
    """
    objects = UserProfileManager()

    # Name of the organization that the user belongs to.
    organization = models.CharField(max_length=100)
    # Country of origin of the organization that the user belongs to.
    country = CountryField()
    # Initially set to false, indicates whether administrator has accepted
    # this user or not.
    is_verified = models.BooleanField()
    
    # Initially set to false, indicates whether network administrator has
    # decided to block the requests from this user.
    is_blocked = models.BooleanField()


class UserSessionManager(models.Manager):
    """
    Custom model manager for the UserSession class
    """
    def getLoggedUsers(self):
        """
        Function that gets all the logged users excluding those who
        are duplicated because they have multiple active sessions (e.g. 
        one from the Chrome client and the other one from the web).
        
        :returns:
            List of django.contrib.auth.models.User classes
        """

        return [ item.user for item in self.distinct('user') ]

class UserSession(models.Model):
    """
    This class holds a list corresponding to the logged users. More details here:
    http://gavinballard.com/associating-django-users-sessions/
    """

    objects = UserSessionManager()

    user = models.ForeignKey(auth_models.User)
    session = models.ForeignKey(Session)