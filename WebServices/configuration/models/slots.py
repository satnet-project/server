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

:Description:

This module contains all the database models for the configuration of the
spacecraft, ground stations and channels.

There is a set of 'base' models that are designed for containing the different
options for the configuration requirements of communications channels. Their
name is ended with 'Options'. This way, users may add new options for
modulations, bitrates and bandwidth as soon as they are needed. Polarization
options may remain fixed to 'Any', 'LHCP' or 'RHCP' at least for the first
releases.

:Author:
    Ricardo Tubio-Pardavila (rtubiopa@calpoly.edu)
"""
__author__ = 'rtubiopa@calpoly.edu'

import logging
logger = logging.getLogger(__name__)
from django.db import models


class OperationalSlots(models.Model):
    """
    This model describes the start and ending of a given slot.
    """

    class Meta:
        app_label = 'configuration'

    initial_date = models.DateTimeField('Initial date for the available slot')
    final_date = models.DateTimeField('Final date for the available slot')
