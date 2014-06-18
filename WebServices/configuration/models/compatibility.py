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

:Author:
    Ricardo Tubio-Pardavila (rtubiopa@calpoly.edu)
"""
__author__ = 'rtubiopa@calpoly.edu'

from django.db import models

from configuration.models.channels import SpacecraftChannel,\
    GroundStationChannel
from configuration.models.segments import SpacecraftConfiguration,\
    GroundStationConfiguration


class SegmentsCompatibilityManager(models.Manager):
    """
    Manager that handles the basic operations over the SegmentsCompatibility
    table.
    """
    pass


class SegmentsCompatibility(models.Model):
    """
    This model permits handle a table where the information about the
    compatibility in between SpacecraftConfiguration, SpacecraftChannel,
    GroundStationChannel and GroundStationConfiguration objects is stored.
    """
    class Meta:
        app_label = 'configuration'

    objects = SegmentsCompatibilityManager()

    spacecraft = models.ForeignKey(
        SpacecraftConfiguration,
        verbose_name='Reference to the compatible Spacecraft.'
    )
    groundstation = models.ForeignKey(
        GroundStationConfiguration,
        verbose_name='Refernce to the compatible Ground Station.'
    )
    spacecraft_channel = models.ForeignKey(
        SpacecraftChannel,
        verbose_name='Reference to the compatible Spacecraft channel.'
    )
    groundstation_channel = models.ManyToManyField(
        GroundStationChannel,
        verbose_name='Reference to all the compatible GroundStation channels.'
    )