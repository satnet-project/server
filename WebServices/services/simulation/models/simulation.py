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

from django.db import models
from djorm_pgarray import fields as pgarray_fields
from services.common import simulation as simulator


class GroundTrackManager(models.Manager):
    """
    Manager for the GroundTracks.
    """

    def create(self, groundtrack):
        pass

    @staticmethod
    def spacecraft_added(sender, instance, **kwargs):
        """
        """
        gt = simulator.OrbitalSimulator.calculate_groundtrack(instance.tle)

    @staticmethod
    def spacecraft_removed(sender, instance, **kwargs):
        """
        """
        pass

    @staticmethod
    def spacecraft_tle_updated(sender, instance, **kwargs):
        """
        """
        pass


class GroundTrack(models.Model):
    """
    Class that represents a GroundTrack for a given Spacecraft over the next
    simulation period.
    """
    class Meta:
        app_label = 'simulation'

    objects = GroundTrackManager()

    latitude = pgarray_fields.FloatArrayField(
        'Latitude for the points of the GroundTrack.'
    )
    longitude = pgarray_fields.FloatArrayField(
        'Longitude for the points of the GroundTrack.'
    )
    timestamp = pgarray_fields.IntegerArrayField(
        'UTC time at which the spacecraft is going to pass over the given point'
        ' of its GroundTrack.'
    )