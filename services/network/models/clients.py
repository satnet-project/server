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

from django.db import models as django_models
import logging
from services.accounts.models import UserProfile

logger = logging.getLogger('network')


class ClientsManager(django_models.Manager):
    """
    Custom model manager for the Clients class
    """
    def get_logged_users(self):
        """
        Function that gets all the logged users excluding those who are
        duplicated because they have multiple active sessions (e.g. one from
        the Chrome client and the other one from the web).

        :returns: List of django.contrib.auth.models.User classes
        """
        return [item.user for item in self.distinct('user')]


class Client(django_models.Model):
    """
    This class holds a list corresponding to the logged users. More details
    here: http://gavinballard.com/associating-django-users-sessions/
    """
    class Meta:
        app_label = 'network'

    objects = ClientsManager()

    user = django_models.ForeignKey(
        UserProfile,
        verbose_name='Reference to the profile of the user'
    )
    is_sw_client = django_models.BooleanField(
        'Defines whether this client is a remote software application or not',
        default=False
    )
