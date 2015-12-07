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

import logging
logger = logging.getLogger('scheduling')
from django import apps as django_apps

from services.scheduling.models import availability as availability_models
from website import settings as sn_settings


class SchedulingConfig(django_apps.AppConfig):
    """django.apps.AppConfig
    Default Django-like application configuration object.
    """
    name = 'services.scheduling'
    verbose_name = 'SaTnet Scheduling Service'

    def ready(self):
        """
        Method to be invoked whenever the database has been fully propagated.
        """

        logger.info('>>> Initializing Scheduling Service')
        if not sn_settings.TESTING:
            availability_models.AvailabilitySlot.objects.propagate_slots()
