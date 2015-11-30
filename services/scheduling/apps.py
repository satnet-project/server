"""
   Copyright 2013, 2014, 2015 Ricardo Tubio-Pardavila

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

from django import apps as django_apps
import logging

from services.scheduling.models import availability as availability_models
from website import settings as sn_settings

logger = logging.getLogger('scheduling')


class SchedulingConfig(django_apps.AppConfig):
    """Django application's configuration class
    Class to use for a complex configuration case rather than importing modules
    at the __init__.py file.
    """

    name = 'services.scheduling'
    verbose_name = 'Scheduling Service'

    def ready(self):
        """
        Default ready method executed everytime the Django server is run after
        the registry has been correctly initialized.
        """

        if not sn_settings.TESTING:

            logger.info('[SCHEDULING CONFIG] Automatically populating slots...')
            availability_models.AvailabilitySlot.objects.propagate_slots()
            logger.info('[SCHEDULING CONFIG] PROPAGATED!')
