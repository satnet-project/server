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

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.db import models
from django_countries.fields import CountryField

from accounts.models import UserProfile
from common.misc import get_altitude
from configuration.models.channels import SpacecraftChannel, \
    GroundStationChannel


class SpacecraftConfigurationManager(models.Manager):
    """
    Manager that contains all the methods required for accessing to the
    contents of the SpacecraftConfiguration database models.
    """

    def add_channel(
        self,
        sc_identifier=None,
        identifier=None,
        frequency=None,
        modulation=None,
        bitrate=None,
        bandwidth=None,
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

        # ### Now we re-calculate the compatibility channels table...
        ChannelsCompatibility.objects.new_sc_channel(sc_ch)

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
        # 2) Before removing the channel object itself, we must update the
        # table for the compatible channels accordingly:
        ChannelsCompatibility.objects.remove_sc_channel(channel_id)
        # 3) Last, but not least, we remove the channel from the database.
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


class SpacecraftConfiguration(models.Model):
    """
    This class models the configuration required for managing any type of
    spacecraft in terms of communications and pass simulations.
    """
    class Meta:
        app_label = 'configuration'

    objects = SpacecraftConfigurationManager()

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


class GroundStationConfigurationManager(models.Manager):
    """
    Manager that contains all the methods required for accessing to the
    contents of the GroundStationConfiguration database models.
    """

    def create(self, latitude, longitude, altitude, **kwargs):
        """
        Method for creating a new GroundStation. This method has to be
        overwritten for incorporating some automatic calculations to be
        carried out by the server instead than by requesting more information
        from the user.
        :return The just-created object.
        """
        altitude = get_altitude(latitude, longitude)[0]
        return super(GroundStationConfigurationManager, self).create(
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
        gsch = GroundStationChannel.objects.create(
            identifier=identifier,
            band=band,
            modulations=modulations,
            bitrates=bitrates,
            bandwidths=bandwidths,
            polarizations=polarizations
        )
        gs.channels.add(gsch)
        gs.save()

        # The table of compatible channels should be adapted
        ChannelsCompatibility.objects.new_gs_channel(identifier)

        return gsch

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

        # 4) Before removing the channel object itself, we must update the
        # table for the compatible channels accordingly:
        ChannelsCompatibility.objects.remove_gs_channel(channel_id)

        # 5) Last, but not least, we remove the channel from the database.
        ch.delete()

    def get_channel(self, ground_station_id, channel_id):
        """
        This method returns the channel identified by the given id that
        belongs to the given GroundStation.
        """
        gs = self.all().get(identifier=ground_station_id)
        return gs.channels.all().get(identifier=channel_id)


class GroundStationConfiguration(models.Model):
    """
    This class models the configuration required for managing a generic ground
    station, in terms of communication channels and pass simulations.
    """
    class Meta:
        app_label = 'configuration'

    objects = GroundStationConfigurationManager()
    user = models.ForeignKey(UserProfile)

    identifier = models.CharField(
        'Identifier', max_length=30, unique=True,
        validators=[RegexValidator(
            regex='^[a-zA-Z0-9.\-_]*$',
            message="Alphanumeric or '.-_' required",
            code='invalid_spacecraft_identifier'
        )]
    )
    callsign = models.CharField(
        'Callsign', max_length=10,
        validators=[RegexValidator(
            regex='^[a-zA-Z0-9.\-_]*$',
            message="Alphanumeric or '.-_' required",
            code='invalid_callsign'
        )]
    )

    contact_elevation = models.DecimalField(
        'Contact elevation (degrees)',
        max_digits=4, decimal_places=2
    )
    longitude = models.FloatField('Longitude of the Ground Station')
    latitude = models.FloatField('Latitude of the Ground Station')
    altitude = models.FloatField('Altitude of the Ground Station.')

    # Necessary for matching this information with the IARU database for band
    # regulations.
    country = CountryField('Country where the GroundStation is located.')
    IARU_region = models.SmallIntegerField('IARU region identifier.')
    # Configure ground station channels.
    channels = models.ManyToManyField(GroundStationChannel)

    def delete(self, using=None):
        """
        Overriden method that deletes this object together with
        all its associated resources.
        """
        self.channels.all().delete()
        super(GroundStationConfiguration, self).delete()

    def update(
        self, callsign=None, contact_elevation=None,
        latitude=None, longitude=None
    ):
        """
        Updates the configuration for the given ground station. It is not
        necessary to provide all the parameters for this function, since only
        those that are not null will be updated.
        """
        if callsign and self.callsign != callsign > 0:
            self.callsign = callsign
        if contact_elevation and self.contact_elevation != contact_elevation\
                > 0:
            self.contact_elevation = contact_elevation
        if latitude and self.latitude != latitude > 0:
            self.latitude = latitude
        if longitude and self.longitude != longitude > 0:
            self.longitude = longitude
        self.save()


class CompatibleChannelsManager(models.Manager):
    """
    Manager for the compatible's channels table.
    """

    @staticmethod
    def find_compatible_gs_channels(sc_ch_id):
        """
        Static method that finds all the compatible GroundStation channels
        with the given Spacecraft channel.
        :param sc_ch_id: The identifier of the Spacecraft channel.
        :return: A query list with the results of the search throughout the
        database.
        """
        sc_ch = SpacecraftChannel.objects.get(identifier=sc_ch_id)

        return GroundStationChannel.objects\
            .filter(enabled=True)\
            .filter(band__IARU_allocation_minimum_frequency__lt=sc_ch
                    .frequency)\
            .filter(band__IARU_allocation_maximum_frequency__gt=sc_ch
                    .frequency)\
            .filter(modulations=sc_ch)\
            .filter(bitrates=sc_ch.bitrate)\
            .filter(bandwidths=sc_ch.bandwidth)\
            .filter(polarizations=sc_ch.polarization)

    @staticmethod
    def find_compatible_sc_channels(gs_ch_id):
        """
        Static method that finds all the compatible Spacecraft channels with
        the given GroundStation channel.
        :param gs_ch_id: The identifier of the GroundStation channel.
        :return: A query list with the results of the search throughout the
        database.
        """
        gs_ch = GroundStationChannel.objects.get(identifier=gs_ch_id)

        return SpacecraftChannel.objects\
            .filter(enabled=True)\
            .filter(frequency__gt=gs_ch.band.IARU_allocation_minimum_frequency)\
            .filter(frequency__lt=gs_ch.band.IARU_allocation_maximum_frequency)\
            .filter(modulation__in=gs_ch.modulations.all())\
            .filter(bitrate__in=gs_ch.bitrates.all())\
            .filter(bandwidth__in=gs_ch.bandwidths.all())\
            .filter(polarization__in=gs_ch.polarizations.all())

    def new_sc_channel(self, sc_ch_id):
        """
        Updates the compatible channels table with this new channel.

        ### FILTERING RULES:
        1) enabled = True
        2) gs_min_frequency < sc_frequency < gs_max_frequency
        3) sc_modulation in [gs_modulation_1, ..., gs_modulation_n]
        4) sc_bitrate in [gs_bitrate_1, ..., gs_bitrate_n]
        5) sc_polarization in [gs_polarization_1, ..., gs_polarization_n] or
              ( gs_polarization == ANY ) or ( sc_polarization == ANY )

        ### (3) filter objects taking into account modulations, exact match
        required from the list of available modulations
        ### (4) filter objects taking into account bitrates, exact match
        required from the list of available bitrates
        ### filter objects taking into account the polarizations implemented by
        the GS (RHPC, LHPC or ANY) and the one required by the spacecraft. In
        this case, the ANY polarization indicates that either the spacecraft
        or the ground station implement/require any value.
        """
        try:
            sc_ch = SpacecraftChannel.objects.get(identifier=sc_ch_id)
            self.get(spacecraft_channel=sc_ch)
            raise Exception('SC Channel <' + str(sc_ch_id) + "> exists!")
        except ObjectDoesNotExist:
            pass

        # 1) first, we get the list of compatible channels with the given one.
        compatible_chs = self\
            .find_compatible_gs_channels(sc_ch_id.identifier)

        # 2) secondly, we include this new "matching" group in the list of
        #       compatible channels
        s = self.create(spacecraft_channel=sc_ch_id)
        s.save()
        s.compatible_groundstation_chs.add(*compatible_chs)
        s.save()

    def remove_sc_channel(self, sc_ch_id):
        """
        Updates the compatible channels table by removing the entries for
        this spacecraft channel that has just been removed from the database.
        :param sc_ch_id: Identifier of the Spacecraft channel to be removed.
        """
        sc_ch = SpacecraftChannel.objects.get(identifier=sc_ch_id)
        self.get(spacecraft_channel=sc_ch).delete()

    def new_gs_channel(self, gs_ch_id):
        """
        Updates the compatible channels table with this new GS channel. This
        means that this function must:

        (1) Get the list of compatible SC channels.
        (2) For each of the compatible SC channels, add itself as a new
            compatible GS channel to the table.
            (*) If this GS channel is already added for one SC channel,
            then just skip to the next row of the table.

        The filtering rules for checking the compatibility of this new GS
        channel with the existing SC channels,

        """
        # 1) first we get the list of the compatible SC channels
        compatible_chs = self.find_compatible_sc_channels(gs_ch_id)
        gs_ch = GroundStationChannel.objects.get(identifier=gs_ch_id)

        # 2) for each of them, we add the new GS channel to its list if it
        # has not been added yet
        for ch_id in compatible_chs:

            c = self.get(spacecraft_channel=ch_id)

            if not gs_ch in c.compatible_groundstation_chs.all():
                c.compatible_groundstation_chs.add(gs_ch)
                c.save()

    def remove_gs_channel(self, gs_ch_id):
        """
        Updates the compatible channels table by removing the entries for
        this GroundStation channel that has just been removed from the database.
        :param gs_ch_id: Identifier of the GroundStation channel to be removed.
        """
        gs_ch = GroundStationChannel.objects.get(identifier=gs_ch_id)
        for c_ch in self.filter(compatible_groundstation_chs=gs_ch):
            c_ch.compatible_groundstation_chs.remove(gs_ch)


class ChannelsCompatibility(models.Model):
    """
    This class models the relationship in between the channels of ground
    stations and spacecraft, this is, is the table used for storing the set
    of compatible pairs SC-GS.
    """
    class Meta:
        app_label = 'configuration'
    objects = CompatibleChannelsManager()

    spacecraft_channel = models.ForeignKey(
        SpacecraftChannel,
        verbose_name='Reference to the channels of the spacecraft.'
    )
    compatible_groundstation_chs = models.ManyToManyField(
        GroundStationChannel,
        verbose_name='GroundStation channel compatible with the SC channel.'
    )