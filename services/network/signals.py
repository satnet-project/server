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
logger = logging.getLogger('network')

from allauth.account import signals as allauth_signals
from django.db.models import signals as django_signals
from django import dispatch as django_dispatch

from services.accounts import models as account_models
from services.configuration.models import segments as segment_models
from services.network.models import server as server_models
from services.network.models import clients as client_models
from website import signals as sn_signals


# noinspection PyUnusedLocal
@django_dispatch.receiver(sn_signals.sn_loaded)
def satnet_loaded(sender, **kwargs):
    """
    Signal that indicates that the application has already been loaded and,
    therefore, the database is ready to be used.
    :param sender: Any sender is accepted
    :param kwargs: Additional parameters
    """
    logger.info(
        '>>> network@satnet_loaded (SIGNAL): Loading local server...'
    )
    server_models.ServerManager().load_local_server()


# noinspection PyUnusedLocal
@django_dispatch.receiver(
    django_signals.post_save,
    sender=segment_models.GroundStation
)
def gs_saved_handler(sender, instance, created, raw, **kwargs):
    """Signal handler.
    Callback invoked whenever a GroundStation object is saved.
    :param sender: Object who sent this signal
    :param instance: Reference to the object
    :param created: Flag indicating whether the object is a new creation
    :param raw: Falg indicating whether the object is raw in the database
    :param kwargs: Additional parameters dictionary from the signal
    """
    if not created or raw:
        return

    local_s = server_models.Server.objects.get_local()
    local_s.groundstations.add(instance)
    local_s.save()


# noinspection PyUnusedLocal
@django_dispatch.receiver(allauth_signals.user_logged_in)
def logged_in_receiver(sender, request, user, **kwargs):
    """User logged int callback
    Callback executed automatically when a new user has just logged in.
    :param sender: Object triggering the execution of this callback
    :param request: The request being sent
    :param user: Reference to the user object that has just logged in
    :param kwargs: Additional arguments
    """
    client_models.Client.objects.get_or_create(
        user=account_models.UserProfile.objects.get(username=user.username)
    )
