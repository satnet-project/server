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

from django.db.models import signals as django_signals
from django import dispatch as django_dispatch
from services.configuration.models import segments as segment_models
from services.network import models as network_models


@django_dispatch.receiver(
    django_signals.post_save,
    sender=segment_models.GroundStation
)
def gs_saved_handler(sender, instance, created, raw, **kwargs):
    """Signal handler.
    Callback invoked whenever a GroundStation object is saved.
    """
    if not created or raw:
        return

    local_s = network_models.Server.objects.get_local()
    local_s.groundstations.add(instance)
    local_s.save()