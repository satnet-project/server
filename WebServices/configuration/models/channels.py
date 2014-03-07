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
from configuration.models.bands import AvailableBands
from configuration.models.rules import AvailabilityRule
from configuration.models.slots import OperationalSlot


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

    class Meta:
        app_label = 'configuration'

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

    class Meta:
        app_label = 'configuration'

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

    class Meta:
        app_label = 'configuration'

    bandwidth = models.DecimalField('Bandwidth (kHz)',
                                    max_digits=24, decimal_places=9)


class AvailablePolarizations(models.Model):
    """
    This class permits the storage in the database of the bandwidth options
    for creating communication channels. This way, the bandwidth field of a 
    Channel object must be filled only with data from this model.
    """

    class Meta:
        app_label = 'configuration'

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

    class Meta:
        app_label = 'configuration'

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
    Model manager that contains method for helping in the management and
    handling of the ground station channel objects stored in the database.
    """

    def create(self, identifier=None, band=None,
               modulations=None, bitrates=None, bandwidths=None,
               polarizations=None):
        """
        Creates a new channel object for a ground station, using the given
        band_name for linking it to an existing band.
        :return: A reference to the just-created channel object.
        """
        gsc = GroundStationChannel(identifier=identifier, band=band)
        gsc.enabled = True
        gsc.save()
        # not all parameters are mandatory, therefore, the object is created
        # even in the case not all these parameters are set.
        if modulations:
            gsc.modulation.add(*modulations)
        if bitrates:
            gsc.bitrate.add(*bitrates)
        if bandwidths:
            gsc.bandwidth.add(*bandwidths)
        if polarizations:
            gsc.polarization.add(*polarizations)
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

    # Rules that define the time availability of a given Ground Station.
    rules = models.ManyToManyField(AvailabilityRule)
    # Slots available in accordance with the given availability rules.
    slots = models.ManyToManyField(OperationalSlot)

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

    def update(self,
               band=None,
               modulations_list=None,
               bitrates_list=None,
               bandwidths_list=None,
               polarizations_list=None):
        """
        Updates the configuration for the given channel. It is not necessary to
        provide all the parameters for this function, since only those that
        are not null will be updated.
        """
        if band and self.band != band:
            self.band = band
        if modulations_list and len(modulations_list) > 0:
            self.modulation.clear()
            self.modulation.add(*modulations_list)
        if bitrates_list and len(bitrates_list) > 0:
            self.bitrate.clear()
            self.bitrate.add(*bitrates_list)
        if bandwidths_list and len(bandwidths_list) > 0:
            self.bandwidth.clear()
            self.bandwidth.add(*bandwidths_list)
        if polarizations_list and len(polarizations_list) > 0:
            self.polarization.clear()
            self.polarization.add(*polarizations_list)
        self.save()
        return self

    def add_rule(self, operation, periodicity, dates):
        """
        This method adds a new rule to this channel.
        :param operation: The type of operation for the rule to be added.
        :param periodicity: The periodicity for the rule.
        :param dates: The dates for the definition of the time intervales in
        accordance with the periodicity of the rule.
        :return: A reference to the object that holds the new rule.
        """

        rule = AvailabilityRule.objects.create(operation=operation,
                                               periodicity=periodicity,
                                               dates=dates)
        self.rules.add(rule)
        return rule

    def remove_rule(self, rule_id):
        """
        This method removes an existing availability rule from this channel.
        :param rule_id: The identifier of the rule to be removed.
        :return: 'True' if the removal process was succesful.
        """
        rule = self.rules.get(id=rule_id)
        self.rules.remove(rule)
        rule.delete()

    def get_rules(self):
        """
        This method returns all the rule objects for this channel.
        :return: Array with the rule objects.
        """
        return self.rules.all()

    def __unicode__(self):
        """
        Unicode representation of the object.
        :returns Unicode string.
        """
        return 'GroundStationChannel, ' \
               'identifier = ' + self.identifier +\
               ', band.pk = ' + self.band.pk
