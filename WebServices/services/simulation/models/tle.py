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

from django.core import exceptions
from django.db import models
import logging
from urllib2 import urlopen as urllib2_urlopen
from services.common import misc
from services.simulation.models.celestrak import CelestrakDatabase as Celestrak

logger = logging.getLogger('simulation')


class TwoLineElementsManager(models.Manager):
    """
    Class that handles all actions related with the TLE database table.
    """

    def create(self, source, l0, l1, l2):
        """
        Overriden create method that adds a new entry in the TLE database
        with the correspondent timestamp about the time of update. The line 0
        of the TLE is used as a identifier for the TLE itself.
        """
        return super(TwoLineElementsManager, self).create(
            timestamp=misc.get_utc_timestamp(),
            identifier=l0,
            first_line=l1,
            second_line=l2,
        )

    def create_or_update(self, source, l0, l1, l2):
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
            tle.dirty_update(source=source, identifier=l0, l1=l1, l2=l2)
        except exceptions.ObjectDoesNotExist:
            self.create(source, l0, l1, l2)

    @staticmethod
    def load_celestrak():
        """
        Loads the TLE from all the accessible database from celestrak.com
        """
        for s_tuple in Celestrak.CELESTRAK_SECTIONS:

            section = s_tuple[0]
            tle_info = s_tuple[1]

            for (url, description) in tle_info:
                TwoLineElementsManager.load_tles(section, url)

    @staticmethod
    def load_tles(
        section=Celestrak.CELESTRAK_SECTION_5,
        url_string=Celestrak.CELESTRAK_CUBESATS,
        debug=False
    ):
        """
        This method loads the TLE's in the database and updates them in
        accordance with the latest information gathered from NORAD's website.
        """
        l_n = 0
        l0, l1, l2 = '', '', ''

        if debug:
            logger.debug(
                '@[load_tles], url_string = ' + str(url_string)
            )

        for l_i in urllib2_urlopen(url_string):

            if l_n % 3 == 0:
                l0 = l_i.rstrip()
            if l_n % 3 == 1:
                l1 = l_i.rstrip()
            if l_n % 3 == 2:
                l2 = l_i.rstrip()

                if debug:
                    logger.debug(
                        '@[load_tles]: section = ' + str(section)
                        + ', id = <' + str(l0) + '>'
                        + ",\n\t l1 = <" + str(l1) + '>'
                        + ",\n\t l2 = <" + str(l2) + '>'
                    )

                TwoLineElement.objects.create_or_update(
                    source=section, l0=l0, l1=l1, l2=l2
                )

            l_n += 1


class TwoLineElement(models.Model):
    """
    Class that models the TLE elements within the database.
    """
    class Meta:
        app_label = 'simulation'

    objects = TwoLineElementsManager()

    identifier = models.CharField(
        'Identifier of the spacecraft that this TLE element models (line 0)',
        max_length=24,
        unique=True
    )

    timestamp = models.BigIntegerField(
        'Timestamp with the update date for this TLE'
    )

    source = models.CharField(
        'String that indicates the source of this TLE',
        max_length=100,
        choices=Celestrak.CELESTRAK_SECTIONS,
        default=Celestrak.CELESTRAK_CUBESATS
    )

    first_line = models.CharField(
        'First line of a given two-line element (line 1)',
        max_length=69
    )
    second_line = models.CharField(
        'Second line of a given two-line element (line 2)',
        max_length=69
    )

    def dirty_update(self, source, identifier, l1, l2):
        """
        Updates the configuration for this TwoLineEelment with the data
        provided.
        :param source: The source for this TLE.
        :param identifier: The identification line of the TLE (line #0).
        :param l1: The first line of the TLE (line#1).
        :param l2: The second line of the TLE (line#2).
        """
        changed_flag = False

        if self.identifier != identifier:
            self.identifier = identifier
            changed_flag = True

        if self.first_line != l1:
            self.first_line = l1
            changed_flag = True

        if self.second_line != l2:
            self.second_line = l2
            changed_flag = True

        if self.source != source:
            self.source = source
            changed_flag = True

        if changed_flag:
            self.timestamp = misc.get_utc_timestamp()
            self.save()