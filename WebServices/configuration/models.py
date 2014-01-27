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

import logging
logger = logging.getLogger(__name__)

from django.core.validators import RegexValidator
from django.db import models

from django_countries.fields import CountryField

from accounts.models import UserProfile
from configuration.models_bands import AvailableBands


class AvailableModulations(models.Model):
    """
    This class permits the storage in the database of the modulation options 
    for creating communication channels. This way, the modulation field of a 
    Channel object must be filled only with data from this model.
    
    MODULATION_CHOICES = (
        ('AFSK', 'Audio Frequency-Shift Keying (AFSK)'),
        ('FSK', 'Frequency-Shift Keying (FSK)'),
        ('GMSK', 'Gaussian Minimum Shift Keying (GMSK)'),
    )
    """

    modulation = models.CharField('Modulation', max_length=9)


class AvailableBitrates(models.Model):
    """
    This class permits the storage in the database of the bitrate options
    for creating communication channels. This way, the bitrate field of a 
    Channel object must be filled only with data from this model.
    
    BITRATE_CHOICES = (
        (300, '300 bps'),
        (600, '600 bps'),
        (900, '900 bps'),        
    )
    
    """

    bitrate = models.IntegerField('Bitrate (bps)')


class AvailableBandwidths(models.Model):
    """
    This class permits the storage in the database of the bandwidth options
    for creating communication channels. This way, the bandwidth field of a 
    Channel object must be filled only with data from this model.
    
    BANDWIDTH_CHOICES = (
        (12.5, '12.500 kHz'),
        (25.0, '25.000 kHz'),
    )
    
    """

    bandwidth = models.DecimalField('Bandwidth (kHz)',
                                    max_digits=24, decimal_places=9)


class AvailablePolarizations(models.Model):
    """
    This class permits the storage in the database of the bandwidth options
    for creating communication channels. This way, the bandwidth field of a 
    Channel object must be filled only with data from this model.
    """
    
    POLARIZATION_CHOICES = (
        ('Any', 'Any polarization type'),
        ('RHCP', 'RHCP polarization'),
        ('LHCP', 'LHCP polarization'),
    )

    polarization = models.CharField('Polarization modes',
                                    max_length=10, choices=POLARIZATION_CHOICES)


class SpacecraftChannel(models.Model):
    """
    This class models the database model for a spacecraft communications 
    channel.
    """
    
    identifier = models.CharField('Unique identifier',
                                  max_length=30, unique=True,
                                  validators=[RegexValidator(
                                      regex='^[a-zA-Z0-9.-_]*$',
                                      message="Alphanumeric or '.-_' required",
                                      code='invalid_channel_identifier')])
    
    modulation = models.ManyToManyField(AvailableModulations)
    bitrate = models.ManyToManyField(AvailableBitrates)
    bandwidth = models.ManyToManyField(AvailableBandwidths)
    polarization = models.ManyToManyField(AvailablePolarizations)
    
    # In Hz, mili-Hz resolution, up to 1 EHz, central frequency
    frequency = models.DecimalField('Central frequency (Hz)',
                                    max_digits=15, decimal_places=3)


class GroundStationChannelManager(models.Manager):
    """
    Manager class for Ground Staiton Channels. It helps in managing channel
    objects.
    """

    def create(self,
               gs_identifier=None, identifier=None, band_name=None,
               modulations_list=None,
               bitrates_list=None,
               bandwidths_list=None,
               polarizations_list=None):
        """
        This method creates a new communications channel and associates it to
        the GroundStation whose identifier is given as a parameter.
        """

        gs = GroundStationConfiguration.objects.get(identifier=gs_identifier)

        band = AvailableBands.objects.get(band_name=band_name)
        gsc = GroundStationChannel(band=band)
        gsc.identifier = identifier
        gsc.band = band
        # by default, channels are saved with the 'enabled' flag set to 'True'
        gsc.enabled = True
        gsc.save()

        gsc.modulation.add(*modulations_list)
        gsc.bitrate.add(*bitrates_list)
        gsc.bandwidth.add(*bandwidths_list)
        gsc.polarization.add(*polarizations_list)
        gsc.save()

        gs.channels.add(gsc)
        gs.save()

        return gsc

    def update(self,
               current_identifier=None,
               identifier=None, band=None,
               modulations_list=None,
               bitrates_list=None,
               bandwidths_list=None,
               polarizations_list=None):
        """
        Updates the configuration for the given channel.
        """

        ch = GroundStationChannel.objects.get(identifier=current_identifier)
        if identifier:
            ch.identifier = identifier
        if band:
            ch.band = band
        if modulations_list and len(modulations_list) > 0:
            ch.modulation.clear()
            ch.modulation.add(*modulations_list)
        if bitrates_list and len(bitrates_list) > 0:
            ch.bitrate.clear()
            ch.bitrate.add(*bitrates_list)
        if bandwidths_list and len(bandwidths_list) > 0:
            ch.bandwidth.clear()
            ch.bandwidth.add(*bandwidths_list)
        if polarizations_list and len(polarizations_list) > 0:
            ch.polarization.clear()
            ch.polarization.add(*polarizations_list)
        ch.save()

        return ch


class GroundStationChannel(models.Model):
    """
    This class models the database model for a ground station communications 
    channel.
    """

    objects = GroundStationChannelManager()

    identifier = models.CharField('Unique identifier',
                                  max_length=30, unique=True,
                                  validators=[RegexValidator(
                                      regex='^[a-zA-Z0-9.-_]*$',
                                      message="Alphanumeric or '.-_' required",
                                      code='invalid_channel_identifier')])

    band = models.ForeignKey(AvailableBands)

    modulation = models.ManyToManyField(AvailableModulations)
    bitrate = models.ManyToManyField(AvailableBitrates)
    bandwidth = models.ManyToManyField(AvailableBandwidths)
    polarization = models.ManyToManyField(AvailablePolarizations)

    enabled = models.BooleanField('Enabled')

    def get_string_definition(self):
        """
        This method returns a string containing all the parameters that define
        this communication channel.
        """
        return self.band.get_band_name() + ', ' +\
            str(self.modulation) + ', ' +\
            str(self.bitrate) + ', ' +\
            str(self.bandwidth) + ', ' +\
            str(self.polarization)

    def __unicode__(self):
        return 'GroundStationChannel, ' \
               'identifier = ' + self.identifier + \
               ', band.pk = ' + self.band.pk


class SpacecraftConfiguration(models.Model):
    """
    This class models the configuration required for managing any type of
    spacecraft in terms of communications and pass simulations.
    """
    
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

    def delete_channel(self, ground_station_id, channel_id):
        """
        Deletes a channel that is owned by this ground station and all its
        associated resources.
        """

        # 1) First, we obtain the objects for the deletion. If they do not
        #       exist, an exception will be raised automatically. This is
        #       also a way for verifying that the given channel is owned by
        #       that ground station.
        gs, ch = self.get_channel(ground_station_id,channel_id)
        # 2) We unlink this channel from the ground station that owned it.
        gs.channels.remove(ch)
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
        return gs, ch


class GroundStationConfiguration(models.Model):
    """
    This class models the configuration required for managing a generic ground
    station, in terms of communication channels and pass simulations.
    """

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

    # Configure ground station channels
    channels = models.ManyToManyField(GroundStationChannel)


class SlotsAvailable(models.Model):
    """
    This model describes the start and ending for a given slot.
    """

    initial_date = models.DateField('Initial date for the available slot')
    final_date = models.DateField('Final date for the available slot')
