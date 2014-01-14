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
    Manager class for Ground Staiton Channels. It helps
    """

    def create(self,
               gs_identifier=None, identifier=None, band=None,
               modulations_list=None,
               bitrates_list=None,
               bandwidths_list=None,
               polarizations_list=None,
               **kwargs):
        """
        This method creates a new communications channel and associates it to
        the GroundStation whose identifier is given as a parameter.
        """
        gs = GroundStationConfiguration.objects.get(identifier=gs_identifier)

        gsc = GroundStationChannel(band=band)
        gsc.identifier = identifier
        gsc.band = band
        # by default, channels are saved enabled
        gsc.enabled = True
        gsc.save()

        mod_l = []
        for e_i in modulations_list:
            mod_l.append(AvailableModulations.objects.get(modulation=e_i))
        bps_l = []
        for e_i in bitrates_list:
            bps_l.append(AvailableBitrates.objects.get(bitrate=e_i))
        bws_l = []
        for e_i in bandwidths_list:
            bws_l.append(AvailableBandwidths.objects.get(bandwidth=e_i))
        pol_l = []
        for e_i in polarizations_list:
            pol_l.append(AvailablePolarizations.objects.get(polarization=e_i))

        gsc.modulation.add(*mod_l)
        gsc.bitrate.add(*bps_l)
        gsc.bandwidth.add(*bws_l)
        gsc.polarization.add(*pol_l)
        gsc.save()

        gs.channels.add(gsc)
        gs.save()


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


class GroundStationConfiguration(models.Model):
    """
    This class models the configuration required for managing a generic ground
    station, in terms of communication channels and pass simulations.
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
