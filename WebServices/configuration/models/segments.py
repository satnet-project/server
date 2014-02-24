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
logger = logging.getLogger(__name__)
from django.core.validators import RegexValidator
from django.db import models
from django_countries.fields import CountryField
from accounts.models import UserProfile
from configuration.models.channels import SpacecraftChannel, \
    GroundStationChannel


class SpacecraftConfiguration(models.Model):
    """
    This class models the configuration required for managing any type of
    spacecraft in terms of communications and pass simulations.
    """
    class Meta:
        app_label = 'configuration'

    user = models.ForeignKey(UserProfile)
    identifier = models.CharField('Identifier', max_length=30, unique=True,
                                  validators=[RegexValidator(
                                      regex='^[a-zA-Z0-9.\-_]*$',
                                      message="Alphanumeric or '.-_' required",
                                      code='invalid_spacecraft_identifier')])
    callsign = models.CharField('Callsign', max_length=10,
                                validators=[RegexValidator(
                                    regex='^[a-zA-Z0-9.\-_]*$',
                                    message="Alphanumeric or '.-_' required",
                                    code='invalid_callsign')])

    celestrak_id = models.CharField('Celestrak identifier', max_length=100)
    # Spacecraft channels
    channels = models.ManyToManyField(SpacecraftChannel)


class GroundStationConfigurationManager(models.Manager):
    """
    Manager that contains all the methods required for accessing to the
    contents of the GroundStationConfiguration database models.
    """

    def add_channel(self, gs_identifier=None, identifier=None, band=None,
                    modulations=None,
                    bitrates=None,
                    bandwidths=None,
                    polarizations=None):
        """
        This method creates a new communications channel and associates it to
        the GroundStation whose identifier is given as a parameter.
        """
        gs = self.get(identifier=gs_identifier)
        gsc = GroundStationChannel.objects\
            .create(identifier=identifier,
                    band=band,
                    modulations=modulations,
                    bitrates=bitrates,
                    bandwidths=bandwidths,
                    polarizations=polarizations)
        gs.channels.add(gsc)
        gs.save()
        return gsc

    def delete_channel(self, ground_station_id, channel_id):
        """
        Deletes a channel that is owned by this ground station and all its
        associated resources.
        """

        # 1) First, we obtain the objects for the deletion. If they do not
        #       exist, an exception will be raised automatically. This is
        #       also a way for verifying that the given channel is owned by
        #       that ground station.
        ch = self.get_channel(ground_station_id, channel_id)
        # 2) We unlink this channel from the ground station that owned it.
        self.get(identifier=ground_station_id).channels.remove(ch)
        # 3) Last, but not least, we remove the channel from the database.
        ch.delete()

    def get_channel(self, ground_station_id, channel_id):
        """
        This method returns both the ground station and its associated channel
        as a tuple. It obtains the channel object by accessing to the list of
        channels associated with the given ground station. Therefore, in case
        either the ground station does not exist or the requested channel is
        not associated with that ground station, an exception will be raised.
        """
        gs = self.all().get(identifier=ground_station_id)
        ch = gs.channels.all().get(identifier=channel_id)
        return ch


class GroundStationConfiguration(models.Model):
    """
    This class models the configuration required for managing a generic ground
    station, in terms of communication channels and pass simulations.
    """
    class Meta:
        app_label = 'configuration'

    objects = GroundStationConfigurationManager()

    user = models.ForeignKey(UserProfile)
    identifier = models.CharField('Identifier', max_length=30, unique=True,
                                  validators=[RegexValidator(
                                      regex='^[a-zA-Z0-9.\-_]*$',
                                      message="Alphanumeric or '.-_' required",
                                      code='invalid_spacecraft_identifier')])
    callsign = models.CharField('Callsign', max_length=10,
                                validators=[RegexValidator(
                                    regex='^[a-zA-Z0-9.\-_]*$',
                                    message="Alphanumeric or '.-_' required",
                                    code='invalid_callsign')])
    contact_elevation \
        = models.DecimalField('Contact elevation (degrees)',
                              max_digits=4, decimal_places=2)
    longitude = models.FloatField()
    latitude = models.FloatField()
    # Necessary for matching this information with the IARU database for band
    # regulations.
    country = CountryField()
    IARU_region = models.SmallIntegerField('IARU region identifier')
    # Configure ground station channels.
    channels = models.ManyToManyField(GroundStationChannel)

    def delete(self, using=None):
        """
        Overriden method that deletes this object together with
        all its associated resources.
        """
        self.channels.all().delete()
        super(GroundStationConfiguration, self).delete()

    def update(self, callsign=None, contact_elevation=None,
               latitude=None, longitude=None):
        """
        Updates the configuration for the given ground station. It is not
        necessary to provide all the parameters for this function, since only
        those that are not null will be updated.
        """
        if callsign and self.callsign != callsign > 0:
            self.callsign = callsign
        if contact_elevation and self.contact_elevation != contact_elevation \
                > 0:
            self.contact_elevation = contact_elevation
        if latitude and self.latitude != latitude > 0:
            self.latitude = latitude
        if longitude and self.longitude != longitude > 0:
            self.longitude = longitude
        self.save()
