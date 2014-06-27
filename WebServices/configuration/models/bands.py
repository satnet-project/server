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

import re
import logging
logger = logging.getLogger(__name__)

from django.db import models


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

    bandwidth = models.DecimalField(
        'Bandwidth (kHz)',
        max_digits=24, decimal_places=9
    )


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

    polarization = models.CharField(
        'Polarization modes',
        max_length=10,
        choices=POLARIZATION_CHOICES
    )


class AvailableBandsManager(models.Manager):
    """
    Manager for carrying out Bands database specific tasks.
    """

    __band_name_separator = ' / '
    __band_name_splits = 4

    def get(self, band_name=None, *args, **kwargs):
        """
        Returns the object whose name band is the one provided. If no band_name
        is provided, it simply returns the result of the overriden get
        method.
        :rtype : AvailableBands object
        """
        if not band_name:
            return super(AvailableBandsManager, self).get(args, kwargs)

        s = re.split(AvailableBandsManager.__band_name_separator, band_name)
        if len(s) != AvailableBandsManager.__band_name_splits:
            raise Exception('<band_name> incorrect, should have '
                            + str(AvailableBandsManager.__band_name_splits)
                            + 'parts, but has ' + str(len(s)))
        qs = self \
            .filter(IARU_range=s[0]) \
            .filter(AMSAT_letter=s[1]) \
            .filter(IARU_allocation_minimum_frequency=s[2]) \
            .get(IARU_allocation_maximum_frequency=s[3])
        if qs is None:
            raise Exception('<band_name> does not exist.')

        return qs


class AvailableBands(models.Model):
    """
    This class permits the definition of the available bands for operating
    spacecraft. Ground Stations will define the bands available for their
    channels and the network will match the
    """

    class Meta:
        app_label = 'configuration'

    IARU_range = models.CharField('IARU Range', max_length=4)
    IARU_band = models.CharField('IARU Band', max_length=6)
    AMSAT_letter = models.CharField('AMSAT Letter', max_length=4)
    IARU_allocation_minimum_frequency =\
        models.DecimalField('Minimum frequency (MHz)',
                            max_digits=24, decimal_places=6)
    IARU_allocation_maximum_frequency =\
        models.DecimalField('Maximum frequency (MHz)',
                            max_digits=24, decimal_places=6)

    uplink = models.BooleanField('Uplink permitted')
    downlink = models.BooleanField('Downlink permitted')

    # Custom model manager
    objects = AvailableBandsManager()

    band_name = ''
    __band_name_separator = ' / '
    __band_name_splits = 4

    def __init__(self, *args, **kwargs):
        """
        Overriden constructor that initializes this object by creating a unique
        band name that is human readable.
        """

        super(AvailableBands, self).__init__(*args, **kwargs)
        self.band_name = self.get_band_name()

    def get_band_name(self):
        """
        Method that defines a unique band name that is also human readable.
        """
        band_name = str(self.IARU_range)\
            + AvailableBands.__band_name_separator
        band_name += str(self.AMSAT_letter)\
            + AvailableBands.__band_name_separator
        band_name += str(self.IARU_allocation_minimum_frequency)\
            + AvailableBands.__band_name_separator
        band_name += str(self.IARU_allocation_maximum_frequency)

        return band_name

    def __unicode__(self):
        return self.get_band_name()
