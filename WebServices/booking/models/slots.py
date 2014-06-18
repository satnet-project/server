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
    This module contains all the database models for the usage of the slots
    within the booking service.

:Author:
    Ricardo Tubio-Pardavila (rtubiopa@calpoly.edu)
"""
__author__ = 'rtubiopa@calpoly.edu'

from django.db import models
from configuration.models.channels import SpacecraftChannel


class BookedTimeSlot(models.Model):
    """
    This model describes a TimeSlot that has been booked by a given
    Spacecraft. It is expected to be part of the GroundStation Configuration
    for each of its channels and to be linked with the Spacecraft that booked
    its utilization.
    """
    class Meta:
        app_label = 'booking'

    initial_date = models.DateTimeField('Initial date for the available slot')
    final_date = models.DateTimeField('Final date for the available slot')

    spacecraft = models.ForeignKey(SpacecraftChannel,
                                   verbose_name='Channel of the Spacecraft '
                                                'for whom all these slots '
                                                'have been booked.')


class PassTimeSlot(models.Model):
    """
    This model describes a TimeSlot used for managing the pass of a
    Spacecraft over a given Ground Station.
    """
    class Meta:
        app_label = 'booking'
