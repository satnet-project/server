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

from django.core.validators import RegexValidator
from django.db import models
from django_countries.fields import CountryField

from accounts.models import UserProfile
from common.gis import get_altitude
from configuration.models.channels import SpacecraftChannel, \
    GroundStationChannel


class SpacecraftManager(models.Manager):
    """
    Manager that contains all the methods required for accessing to the
    contents of the SpacecraftConfiguration database models.
    """

    def add_channel(
        self, sc_identifier=None, identifier=None,
        frequency=None, modulation=None, bitrate=None, bandwidth=None,
        polarization=None
    ):
        """
        This method creates a new communications channel and associates it to
        the Spacecraft whose identifier is given as a parameter.
        """
        sc = self.get(identifier=sc_identifier)
        sc_ch = SpacecraftChannel.objects.create(
            identifier=identifier,
            frequency=frequency,
            modulation=modulation,
            bitrate=bitrate,
            bandwidth=bandwidth,
            polarization=polarization,
            enabled=True
        )
        sc.channels.add(sc_ch)
        sc.save()
        return sc_ch

    def delete_channel(self, spacecraft_id, channel_id):
        """
        Deletes a channel that is owned by this ground station and all its
        associated resources.
        """

        # 1) First, we obtain the objects for the deletion. If they do not
        #       exist, an exception will be raised automatically. This is
        #       also a way for verifying that the given channel is owned by
        #       that ground station.
        ch = self.get_channel(spacecraft_id, channel_id)
        # 2) Last, but not least, we remove the channel from the database.
        self.get(identifier=spacecraft_id).channels.remove(ch)
        ch.delete()

    def get_channel(self, spacecraft_id, channel_id):
        """
        This method returns both the ground station and its associated channel
        as a tuple. It obtains the channel object by accessing to the list of
        channels associated with the given ground station. Therefore, in case
        either the ground station does not exist or the requested channel is
        not associated with that ground station, an exception will be raised.
        """
        gs = self.all().get(identifier=spacecraft_id)
        return gs.channels.all().get(identifier=channel_id)


class Spacecraft(models.Model):
    """
    This class models the configuration required for managing any type of
    spacecraft in terms of communications and pass simulations.
    """
    class Meta:
        app_label = 'configuration'

    objects = SpacecraftManager()

    user = models.ForeignKey(UserProfile)
    identifier = models.CharField(
        'Identifier',
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex='^[a-zA-Z0-9.\-_]*$',
            message="Alphanumeric or '.-_' required",
            code='invalid_spacecraft_identifier'
        )]
    )
    callsign = models.CharField(
        'Radio amateur callsign',
        max_length=10,
        validators=[RegexValidator(
            regex='^[a-zA-Z0-9.\-_]*$',
            message="Alphanumeric or '.-_' required",
            code='invalid_callsign'
        )]
    )

    tle_id = models.CharField('TLE identifier', max_length=100)
    # Spacecraft channels
    channels = models.ManyToManyField(SpacecraftChannel)

    def update(self, callsign=None, tle_id=None):
        """
        Updates the configuration for the given GroundStation object. It is not
        necessary to provide all the parameters for this function, since only
        those that are not null will be updated.
        """
        changes = False

        if callsign and self.callsign != callsign:
            self.callsign = callsign
            changes = True
        if tle_id and self.tle_id != tle_id:
            self.tle_id = tle_id
            changes = True

        if changes:
            self.save()


class GroundStationsManager(models.Manager):
    """
    Manager that contains all the methods required for accessing to the
    contents of the GroundStationConfiguration database models.
    """

    def create(self, latitude, longitude, altitude=None, **kwargs):
        """
        Method for creating a new GroundStation. This method has to be
        overwritten for incorporating some automatic calculations to be
        carried out by the server instead than by requesting more information
        from the user.
        :return The just-created object.
        """
        if altitude is None:
            altitude = get_altitude(latitude, longitude)[0]
        return super(GroundStationsManager, self).create(
            latitude=latitude,
            longitude=longitude,
            altitude=altitude,
            **kwargs
        )

    def add_channel(
        self, gs_identifier=None, identifier=None, band=None,
        modulations=None, bitrates=None, bandwidths=None, polarizations=None
    ):
        """
        This method creates a new communications channel and associates it to
        the GroundStation whose identifier is given as a parameter.
        """
        gs = self.get(identifier=gs_identifier)
        gs_channel = GroundStationChannel.objects.create(
            identifier=identifier,
            band=band,
            modulations=modulations,
            bitrates=bitrates,
            bandwidths=bandwidths,
            polarizations=polarizations
        )
        gs.channels.add(gs_channel)
        gs.save()
        return gs_channel

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

        # 3) We have to clear all the many-to-many relations for this object
        ch.modulations.clear()
        ch.bitrates.clear()
        ch.bandwidths.clear()
        ch.polarizations.clear()

        # 4) Last, but not least, we remove the channel from the database.
        ch.delete()

    def get_channel(self, ground_station_id, channel_id):
        """
        This method returns the channel identified by the given id that
        belongs to the given GroundStation.
        """
        gs = self.all().get(identifier=ground_station_id)
        return gs.channels.all().get(identifier=channel_id)


class GroundStation(models.Model):
    """
    This class models the configuration required for managing a generic ground
    station, in terms of communication channels and pass simulations.
    """
    class Meta:
        app_label = 'configuration'

    objects = GroundStationsManager()

    user = models.ForeignKey(
        UserProfile,
        verbose_name='User to which this GroundStation belongs to'
    )

    identifier = models.CharField(
        'Unique alphanumeric identifier for this GroundStation',
        max_length=30,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9.\-_]*$',
                message="Alphanumeric or '.-_' required",
                code='invalid_spacecraft_identifier'
            )
        ]
    )
    callsign = models.CharField(
        'Radio amateur callsign for this GroundStation',
        max_length=10,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9.\-_]*$',
                message="Alphanumeric or '.-_' required",
                code='invalid_callsign'
            )
        ]
    )

    contact_elevation = models.FloatField(
        'Minimum elevation for contact(degrees)'
    )
    latitude = models.FloatField('Latitude of the Ground Station')
    longitude = models.FloatField('Longitude of the Ground Station')
    altitude = models.FloatField('Altitude of the Ground Station')

    # Necessary for matching this information with the IARU database for band
    # regulations.
    country = CountryField('Country where the GroundStation is located')
    IARU_region = models.SmallIntegerField('IARU region identifier')

    channels = models.ManyToManyField(
        GroundStationChannel,
        verbose_name='Communication channels that belong to this GroundStation'
    )

    def delete(self, using=None):
        """
        Overriden method that deletes this object together with
        all its associated resources.
        """
        self.channels.all().delete()
        super(GroundStation, self).delete()

    def update(
        self, callsign=None,
        contact_elevation=None,
        latitude=None, longitude=None
    ):
        """
        Updates the configuration for the given GroundStation object. It is not
        necessary to provide all the parameters for this function, since only
        those that are not null will be updated.
        """
        changes = False
        change_altitude = False

        if callsign and self.callsign != callsign:
            self.callsign = callsign
            changes = True
        if not contact_elevation is None and\
                self.contact_elevation != contact_elevation:
            self.contact_elevation = contact_elevation
            changes = True
        if latitude and self.latitude != latitude:
            self.latitude = latitude
            changes = True
            change_altitude = True
        if longitude and self.longitude != longitude:
            self.longitude = longitude
            changes = True
            change_altitude = True

        if change_altitude:
            self.altitude = get_altitude(self.latitude, self.longitude)[0]
        if changes:
            self.save()