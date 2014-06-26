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

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from urllib2 import urlopen as urllib2_urlopen

from common import misc
from configuration.models.segments import Spacecraft


class TwoLineElementsManager(models.Manager):
    """
    Class that handles all actions related with the TLE database table.
    """

    def create(self, l0, l1, l2):
        """
        Overriden create method that adds a new entry in the TLE database
        with the correspondent timestamp about the time of update. The line 0
        of the TLE is used as a identifier for the TLE itself.
        """
        spacecraft = None

        try:
            spacecraft = Spacecraft.objects.get(tle_id=l0)
        except ObjectDoesNotExist:
            spacecraft = None

        return super(TwoLineElementsManager, self).create(
            timestamp=misc.get_utc_timestamp(),
            identifier=l0,
            first_line=l1,
            second_line=l2,
            spacecraft=spacecraft
        )

    def create_or_update(self, l0, l1, l2):
        """
        This method creates the new entry in the databse (in case it does not
        exist); otherwise, it updates the existing entry with the given data
        (if necessary).
        :param l0:
        :param l1:
        :param l2:
        :return:
        """
        try:
            tle = self.get(identifier=l0)
            tle.update(l0=l0, l1=l1, l2=l2)
        except ObjectDoesNotExist:
            self.create(l0, l1, l2)

    __NORAD_CUBESAT_TLE_URL = 'http://celestrak.com/NORAD/elements/cubesat.txt'

    @staticmethod
    def load_tles(url_string=__NORAD_CUBESAT_TLE_URL):
        """
        This method loads the TLE's in the database and updates them in
        accordance with the latest information gathered from NORAD's website.
        """
        l_n = 0
        l0, l1, l2 = '', '', ''

        for l_i in urllib2_urlopen(url_string):

            if l_n % 3 == 0:
                l0 = l_i.rstrip()
            if l_n % 3 == 1:
                l1 = l_i.rstrip()
            if l_n % 3 == 2:
                TwoLineElement.objects.create_or_update(l0, l1, l_i.rstrip())

            l_n += 1

    @staticmethod
    def spacecraft_added(sender, instance, **kwargs):
        """
        Callback handler for the signal coming from the Spacecraft table that
        indicates that a new satellite has been added to the system.
        """
        try:
            tle = TwoLineElement.objects.get(identifier=instance.tle_id)
            tle.spacecraft = instance
            tle.save()
        except ObjectDoesNotExist:
            logger.warning(
                'Cannot find spacecraft in database, sc = ' + str(instance)
            )

    @staticmethod
    def spacecraft_removed(sender, instance, **kwargs):
        """
        Callback handler for the signal coming from the Spacecraft table that
        indicates that a new satellite has been removed from the system.
        """
        try:
            tle = TwoLineElement.objects.get(identifier=instance.tle_id)
            tle.spacecraft = None
            tle.save()
        except ObjectDoesNotExist:
            logger.warning(
                'Cannot find spacecraft in database, sc = ' + str(instance)
            )


class TwoLineElement(models.Model):
    """
    Class that models the TLE elements within the database.
    """
    class Meta:
        app_label = 'booking'

    objects = TwoLineElementsManager()

    timestamp = models.BigIntegerField(
        'Timestamp with the update date for this TLE'
    )

    identifier = models.CharField(
        'Identifier of the spacecraft that this TLE element models (line 0)',
        max_length=24,
        unique=True
    )
    first_line = models.CharField(
        'First line of a given two-line element (line 1)',
        max_length=69
    )
    second_line = models.CharField(
        'Second line of a given two-line element (line 2)',
        max_length=69
    )

    spacecraft = models.ForeignKey(
        Spacecraft,
        null=True,
        blank=True,
        verbose_name='Spacecraft object that requires this TLE'
    )

    def update(self, l0, l1, l2):
        """
        Updates the configuration for this TwoLineEelment with the data
        provided.
        :param l0: The identification line of the TLE (line #0).
        :param l1: The first line of the TLE (line#1).
        :param l2: The second line of the TLE (line#2).
        """
        changed_flag = False

        if self.identifier != l0:
            self.identifier = l0
            changed_flag = True

        if self.first_line != l1:
            self.first_line = l1
            changed_flag = True

        if self.second_line != l2:
            self.second_line = l2
            changed_flag = True

        try:

            sc = Spacecraft.objects.get(tle_id=l0)
            if self.spacecraft.identifier != sc.identifier:
                self.spacecraft = sc
                changed_flag = True

        except ObjectDoesNotExist:

            if self.spacecraft is not None:
                self.spacecraft = None
                changed_flag = True

        if changed_flag:
            self.timestamp = misc.get_utc_timestamp()
            self.save()