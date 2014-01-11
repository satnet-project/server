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


class BandsManager(models.Manager):
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
        """

        if not band_name:
            return super(BandsManager, self).get(args, kwargs)

        s = re.split(BandsManager.__band_name_separator, band_name)
        if len(s) != BandsManager.__band_name_splits:
            raise Exception('<band_name> incorrect, should have '
                            + str(BandsManager.__band_name_splits)
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
    spacecraft. Ground Stations will define the bands available for their channels
    and the network will match the
    """

    IARU_range = models.CharField('IARU Range', max_length=4)
    IARU_band = models.CharField('IARU Band', max_length=6)
    AMSAT_letter = models.CharField('AMSAT Letter', max_length=4)
    IARU_allocation_minimum_frequency =\
        models.DecimalField('Minimum frequency (MHz)',
                            max_digits='24', decimal_places='6')
    IARU_allocation_maximum_frequency =\
        models.DecimalField('Maximum frequency (MHz)',
                            max_digits='24', decimal_places='6')

    uplink = models.BooleanField('Uplink permitted')
    downlink = models.BooleanField('Downlink permitted')

    # Custom model manager
    objects = BandsManager()

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

        band_name = str(self.IARU_range) \
               + AvailableBands.__band_name_separator
        band_name += str(self.AMSAT_letter) \
               + AvailableBands.__band_name_separator
        band_name += str(self.IARU_allocation_minimum_frequency) \
               + AvailableBands.__band_name_separator
        band_name += str(self.IARU_allocation_maximum_frequency)

        return band_name

    def __unicode__(self):
        return self.get_band_name()
