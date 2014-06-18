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

from django.core.validators import RegexValidator
from django.db import models

from configuration.models.bands import AvailableBands, AvailableModulations, \
    AvailableBitrates, AvailableBandwidths, AvailablePolarizations


class SpacecraftChannel(models.Model):
    """
    This class models the database model for a spacecraft communications 
    channel.
    """
    class Meta:
        app_label = 'configuration'

    # ### Channel management parameters
    enabled = models.BooleanField('Enables the usage of this channel.')
    identifier = models.CharField(
        'Unique identifier',
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex='^[a-zA-Z0-9.-_]*$',
            message="Alphanumeric or '.-_' required",
            code='invalid_channel_identifier'
        )]
    )

    # ### Radio characteristics of the channel (common)
    modulation = models.ForeignKey(AvailableModulations)
    bitrate = models.ForeignKey(AvailableBitrates)
    bandwidth = models.ForeignKey(AvailableBandwidths)
    polarization = models.ForeignKey(AvailablePolarizations)
    
    # In Hz, mili-Hz resolution, up to 1 EHz, central frequency
    frequency = models.DecimalField('Central frequency (Hz)',
                                    max_digits=15, decimal_places=3)

    def get_string_definition(self):
        """
        This method returns a string containing all the parameters that define
        this communication channel.
        """
        return str(self.frequency) + ', ' +\
            str(self.modulation) + ', ' +\
            str(self.bitrate) + ', ' +\
            str(self.bandwidth) + ', ' +\
            str(self.polarization)

    def update(
        self, frequency=None,
        modulation=None, bitrate=None, bandwidth=None,
        polarization=None
    ):
        """
        Updates the configuration for the given channel. It is not necessary to
        provide all the parameters for this function, since only those that
        are not null will be updated.
        """
        if frequency and self.frequency != frequency:
            self.frequency = frequency
        self.modulation = modulation
        self.bitrate = bitrate
        self.bandwidth = bandwidth
        self.polarization = polarization
        self.save()
        return self

    def __unicode__(self):
        """
        Unicode representation of the object.
        :returns Unicode string.
        """
        return 'GroundStationChannel' \
               ', identifier = ' + self.identifier +\
               ', frequency = ' + str(self.frequency)


class GroundStationChannelManager(models.Manager):
    """
    Model manager that contains method for helping in the management and
    handling of the ground station channel objects stored in the database.
    """

    def create(
        self, identifier=None, band=None,
        modulations=None, bitrates=None, bandwidths=None, polarizations=None
    ):
        """
        Creates a new channel object for a ground station, using the given
        band_name for linking it to an existing band.
        :return: A reference to the just-created channel object.
        """
        gsc = super(GroundStationChannelManager, self).create(
            identifier=identifier, band=band, enabled=True
        )

        # not all parameters are mandatory, therefore, the object is created
        # even in the case not all these parameters are set.
        if modulations:
            gsc.modulations.add(*modulations)
        if bitrates:
            gsc.bitrates.add(*bitrates)
        if bandwidths:
            gsc.bandwidths.add(*bandwidths)
        if polarizations:
            gsc.polarizations.add(*polarizations)
        gsc.save()
        return gsc


class GroundStationChannel(models.Model):
    """
    This class models the database model for a ground station communications 
    channel.
    """
    class Meta:
        app_label = 'configuration'
    objects = GroundStationChannelManager()

    # ### Channel management parameters
    enabled = models.BooleanField('Enables the usage of this channel.')
    identifier = models.CharField(
        'Unique identifier',
        max_length=30, unique=True,
        validators=[RegexValidator(
            regex='^[a-zA-Z0-9.-_]*$',
            message="Alphanumeric or '.-_' required",
            code='invalid_channel_identifier'
        )]
    )

    band = models.ForeignKey(AvailableBands)

    # ### Radio parameters for a channel.
    modulations = models.ManyToManyField(AvailableModulations)
    bitrates = models.ManyToManyField(AvailableBitrates)
    bandwidths = models.ManyToManyField(AvailableBandwidths)
    polarizations = models.ManyToManyField(AvailablePolarizations)

    def get_string_definition(self):
        """
        This method returns a string containing all the parameters that define
        this communication channel.
        """
        return self.band.get_band_name() + ', ' +\
            str(self.modulations) + ', ' +\
            str(self.bitrates) + ', ' +\
            str(self.bandwidths) + ', ' +\
            str(self.polarizations)

    def update(
            self, band=None,
            modulations_list=None,
            bitrates_list=None,
            bandwidths_list=None,
            polarizations_list=None
    ):
        """
        Updates the configuration for the given channel. It is not necessary to
        provide all the parameters for this function, since only those that
        are not null will be updated.
        """
        if band and self.band != band:
            self.band = band
        if modulations_list and len(modulations_list) > 0:
            self.modulations.clear()
            self.modulations.add(*modulations_list)
        if bitrates_list and len(bitrates_list) > 0:
            self.bitrates.clear()
            self.bitrates.add(*bitrates_list)
        if bandwidths_list and len(bandwidths_list) > 0:
            self.bandwidths.clear()
            self.bandwidths.add(*bandwidths_list)
        if polarizations_list and len(polarizations_list) > 0:
            self.polarizations.clear()
            self.polarizations.add(*polarizations_list)
        self.save()
        return self

    def __unicode__(self):
        """
        Unicode representation of the object.
        :returns Unicode string.
        """
        return 'GroundStationChannel' \
               ', identifier = ' + self.identifier +\
               ', band.pk = ' + str(self.band.pk)