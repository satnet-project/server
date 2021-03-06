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
"""
__author__ = 'rtubiopa@calpoly.edu'

from django.core import validators
from django.db import models

from services.configuration.models import bands as band_models
from services.configuration.models import segments as segment_models


class SpacecraftChannelManager(models.Manager):
    """
    Manager for the objects within the SpacecraftChannel table in the database.
    """

    def find_compatible(self, channel):
        """
        Finds all the compatible Spacecraft channels with the given
        GroundStation channel.
        :param channel: A GroundStation channel object.
        :return: A query list with the results of the search throughout the
        database.
        """

        return self.filter(
            enabled=True
        ).filter(
            frequency__gt=channel.band.IARU_allocation_minimum_frequency
        ).filter(
            frequency__lt=channel.band.IARU_allocation_maximum_frequency
        ).filter(
            modulation__in=channel.modulations.all()
        ).filter(
            bitrate__in=channel.bitrates.all()
        ).filter(
            bandwidth__in=channel.bandwidths.all()
        ).filter(
            polarization__in=channel.polarizations.all()
        )


class SpacecraftChannel(models.Model):
    """
    This class models the database model for a spacecraft communications 
    channel.
    """
    class Meta:
        app_label = 'configuration'

    objects = SpacecraftChannelManager()

    enabled = models.BooleanField(
        'Enables the usage of this channel',
        default=True
    )

    identifier = models.CharField(
        'Unique identifier',
        max_length=30,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex='^[a-zA-Z0-9.-_]*$',
                message="Alphanumeric or '.-_' required",
                code='invalid_channel_identifier'
            )
        ]
    )

    spacecraft = models.ForeignKey(
        segment_models.Spacecraft,
        verbose_name='Spacecraft that this channel belongs to',
        default=1
    )

    modulation = models.ForeignKey(band_models.AvailableModulations)
    bitrate = models.ForeignKey(band_models.AvailableBitrates)
    bandwidth = models.ForeignKey(band_models.AvailableBandwidths)
    polarization = models.ForeignKey(band_models.AvailablePolarizations)

    frequency = models.DecimalField(
        'Central frequency (Hz)', max_digits=15, decimal_places=3
    )

    def get_string_definition(self):
        """
        This method returns a string containing all the parameters that define
        this communication channel.
        """
        return str(
            self.frequency
        ) + ', ' + str(
            self.modulation
        ) + ', ' + str(
            self.bitrate
        ) + ', ' + str(
            self.bandwidth
        ) + ', ' + str(
            self.polarization
        )

    def update(
        self,
        frequency=None,
        modulation=None, bitrate=None, bandwidth=None, polarization=None
    ):
        """
        Updates the configuration for the given channel. It is not necessary to
        provide all the parameters for this function, since only those that
        are not null will be updated.

        :param frequency: The central frequency of the channel
        :param modulation: The modulation of the channel
        :param bitrate: The bitrate of the channel
        :param bandwidth: The bandwidth of the channel
        :param polarization: The polarization of the channel
        """
        if frequency and self.frequency != frequency:
            self.frequency = frequency

        self.modulation = modulation
        self.bitrate = bitrate
        self.bandwidth = bandwidth
        self.polarization = polarization
        self.save()

        return self

    def __str__(self):
        """
        Unicode representation of the object.
        :returns Unicode string.
        """
        return self.get_string_definition()

    # noinspection PyProtectedMember
    @staticmethod
    def get_app_label():
        """
        Returns the app_label of the database.
        """
        return SpacecraftChannel._meta.app_label


class GroundStationChannelManager(models.Manager):
    """
    Model manager that contains method for helping in the management and
    handling of the ground station channel objects stored in the database.
    """

    def create(
        self,
        modulations=None, bitrates=None, bandwidths=None, polarizations=None,
        **kwargs
    ):
        """
        Creates a new channel object for a ground station, using the given
        band_name for linking it to an existing band.

        :param modulations: The modulations of the channel
        :param bitrates: The bitrate of the channel
        :param bandwidths: The bandwidth of the channel
        :param polarizations: The polarization of the channel
        :param kwargs: Additional parameters dictionary
        :return: A reference to the just-created channel object
        """
        gs_ch = super(GroundStationChannelManager, self).create(
            enabled=True, **kwargs
        )

        # not all parameters are mandatory, therefore, the object is created
        # even in the case not all these parameters are set.
        if modulations:
            gs_ch.modulations.add(*modulations)
        if bitrates:
            gs_ch.bitrates.add(*bitrates)
        if bandwidths:
            gs_ch.bandwidths.add(*bandwidths)
        if polarizations:
            gs_ch.polarizations.add(*polarizations)
        gs_ch.save()
        return gs_ch

    @staticmethod
    def find_compatible(sc_channel):
        """
        Static method that finds all the compatible GroundStation channels
        with the given Spacecraft channel.
        :param sc_channel: A SpacecraftChannel object.
        :return: A query list with the results of the search throughout the
        database.
        """
        return GroundStationChannel.objects.filter(
            enabled=True
        ).filter(
            band__IARU_allocation_minimum_frequency__lt=sc_channel.frequency
        ).filter(
            band__IARU_allocation_maximum_frequency__gt=sc_channel.frequency
        ).filter(
            modulations=sc_channel.modulation
        ).filter(
            bitrates=sc_channel.bitrate
        ).filter(
            bandwidths=sc_channel.bandwidth
        ).filter(
            polarizations=sc_channel.polarization
        )


class GroundStationChannel(models.Model):
    """
    This class models the database model for a ground station communications 
    channel.
    """
    class Meta:
        app_label = 'configuration'

    objects = GroundStationChannelManager()

    enabled = models.BooleanField(
        'Enables the usage of this channel',
        default=True
    )

    identifier = models.CharField(
        'Unique identifier',
        max_length=30,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex='^[a-zA-Z0-9.-_]*$',
                message="Alphanumeric or '.-_' required",
                code='invalid_channel_identifier'
            )
        ]
    )

    groundstation = models.ForeignKey(
        segment_models.GroundStation,
        verbose_name='Ground Station that this channel belongs to',
        default=1
    )

    automated = models.BooleanField(
        'Defines this channel as fully automated',
        default=False
    )

    band = models.ForeignKey(
        band_models.AvailableBands,
        verbose_name='Band for the channel of the Ground Station'
    )

    modulations = models.ManyToManyField(band_models.AvailableModulations)
    bitrates = models.ManyToManyField(band_models.AvailableBitrates)
    bandwidths = models.ManyToManyField(band_models.AvailableBandwidths)
    polarizations = models.ManyToManyField(band_models.AvailablePolarizations)

    def get_string_definition(self):
        """
        This method returns a string containing all the parameters that define
        this communication channel.
        """
        return self.band.get_band_name() + ', ' + str(
            self.modulations
        ) + ', ' + str(
            self.bitrates
        ) + ', ' + str(
            self.bandwidths
        ) + ', ' + str(
            self.polarizations
        )

    def update(
        self,
        band=None, automated=None,
        modulations=None, bitrates=None, bandwidths=None, polarizations=None
    ):
        """
        Updates the configuration for the given channel. It is not necessary to
        provide all the parameters for this function, since only those that
        are not null will be updated.

        :param band: Band for the channel
        :param automated: Flag that indicates whether this GS is automated
        :param modulations: The modulations of the channel
        :param bitrates: The bitrate of the channel
        :param bandwidths: The bandwidth of the channel
        :param polarizations: The polarization of the channel
        """
        change = False

        if band and self.band != band:
            self.band = band
            change = True
        if automated and self.automated != automated:
            self.automated = automated
            change = True
        if modulations and len(modulations) > 0:
            self.modulations.clear()
            self.modulations.add(*modulations)
            change = True
        if bitrates and len(bitrates) > 0:
            self.bitrates.clear()
            self.bitrates.add(*bitrates)
            change = True
        if bandwidths and len(bandwidths) > 0:
            self.bandwidths.clear()
            self.bandwidths.add(*bandwidths)
            change = True
        if polarizations and len(polarizations) > 0:
            self.polarizations.clear()
            self.polarizations.add(*polarizations)
            change = True

        if change:
            self.save()

        return self

    def __str__(self):
        """
        Unicode representation of the object.
        :returns Unicode string.
        """
        return str(
            self.__class__.__name__
        ) + ', identifier = ' + str(
            self.identifier
        ) + ', enabled = ' + str(
            self.enabled
        ) + ', band.pk = ' + str(
            self.band.get_band_name()
        ) + ', modulations = ' + str(
            self.modulations.all()
        ) + ', bitrates = ' + str(
            self.bitrates.all()
        ) + ', polarizations = ' + str(
            self.polarizations.all()
        )

    # noinspection PyProtectedMember
    @staticmethod
    def get_app_label():
        """
        Returns the app_label of the database.
        """
        return GroundStationChannel._meta.app_label
