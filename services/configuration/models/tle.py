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
import sys
from urllib.request import urlopen as urllib2_urlopen
from django.core import exceptions, validators
from django.db import models
from services.common import misc
from services.common import simulation
from services.configuration.models.celestrak\
    import CelestrakDatabase as Celestrak

logger = logging.getLogger('configuration')


class TwoLineElementsManager(models.Manager):
    """
    Class that handles all actions related with the TLE database table.
    """
    def create(self, source, l0, l1, l2):
        """
        Overriden create method that adds a new entry in the TLE database
        with the correspondent timestamp about the time of update. The line 0
        of the TLE is used as a identifier for the TLE itself.

        :param source: Link to the source for the TLE
        :param l0: Line #0 of the TLE (identifier)
        :param l1: Line #1 of the TLE
        :param l2: Line #2 of the TLE
        """
        simulation.OrbitalSimulator.check_tle_format(l0, l1, l2)

        return super(TwoLineElementsManager, self).create(
            timestamp=misc.get_utc_timestamp(),
            source=source,
            identifier=l0,
            first_line=l1,
            second_line=l2,
        )

    def create_or_update(self, source, l0, l1, l2):
        """
        This method creates the new entry in the databse (in case it does not
        exist); otherwise, it updates the existing entry with the given data
        (if necessary).

        :param source: Link to the source for the TLE
        :param l0: Line #0 of the TLE (identifier)
        :param l1: Line #1 of the TLE
        :param l2: Line #2 of the TLE
        :return: a reference to the newly created object in the databse.
        """
        try:
            tle = self.get(identifier=l0)
            return tle.dirty_update(source=source, identifier=l0, l1=l1, l2=l2)
        except exceptions.ObjectDoesNotExist:
            return self.create(source, l0, l1, l2)

    POLYSAT_URL = 'https://satnet.aero.calpoly.edu/celestrak/cubesat.txt'

    @staticmethod
    def load_polysat():
        """
        Loads the TLEs from internal polysat resources.
        """
        TwoLineElementsManager.load_tles(
            source=TwoLineElementsManager.POLYSAT_URL
        )

    @staticmethod
    def load_celestrak():
        """
        Loads the TLE from all the accessible resources from celestrak.com
        """
        for s_tuple in Celestrak.CELESTRAK_SECTIONS:

            sys.stdout.write('*')
            sys.stdout.flush()
            # noinspection PyUnusedLocal
            section = s_tuple[0]
            tle_info = s_tuple[1]

            for (url, description) in tle_info:
                sys.stdout.write('.')
                sys.stdout.flush()
                TwoLineElementsManager.load_tles(source=url)

    @staticmethod
    def load_tles(source=Celestrak.CELESTRAK_CUBESATS, testing=False):
        """
        This method loads the TLE's in the database and updates them in
        accordance with the latest information gathered from NORAD's website.

        :param source: URL to the file with the TLE's
        :param testing: Flag that indicates an internal testing state
        """
        l_n = 0
        l0, l1, l2 = '', '', ''

        for l_i in urllib2_urlopen(source):

            if l_n % 3 == 0:
                l0 = l_i.rstrip()
                l_n += 1
                continue

            if l_n % 3 == 1:
                l1 = l_i.rstrip()
                l_n += 1
                continue

            if l_n % 3 == 2:
                l2 = l_i.rstrip()
                l_n += 1

            try:
                TwoLineElement.objects.create_or_update(
                    source=source, l0=l0, l1=l1, l2=l2
                )
            except ValueError as ex:
                if testing:
                    logger.warn('Error reading TLE = ' + str(l0))
                    continue
                else:
                    raise ex


class TwoLineElement(models.Model):
    """TLE database model.
    Class that models the TLE elements within the database.
    """
    class Meta:
        app_label = 'configuration'
        ordering = ['identifier']

    MAX_TLE_ID_LEN = 24
    MAX_TLE_LINE_LEN = 69

    objects = TwoLineElementsManager()

    identifier = models.CharField(
        'Identifier of the spacecraft that this TLE element models (line 0)',
        max_length=24,
        unique=True
    )

    timestamp = models.BigIntegerField(
        'Timestamp with the update date for this TLE'
    )

    source = models.TextField(
        'String that indicates the source of this TLE',
        max_length=100,
        validators=[validators.URLValidator()]
    )

    first_line = models.CharField(
        'First line of this TLE',
        max_length=MAX_TLE_LINE_LEN,
        validators=[
            validators.RegexValidator(
                regex='^[a-zA-Z0-9.\s-]{69}$',
                message="Alphanumeric or '.-_' required",
                code='invalid_tle_line_1'
            )
        ]
    )
    second_line = models.CharField(
        'Second line of this TLE',
        max_length=MAX_TLE_LINE_LEN,
        validators=[
            validators.RegexValidator(
                regex='^[a-zA-Z0-9.\s-]{69}$',
                message="Alphanumeric or '.-_' required",
                code='invalid_tle_line_2'
            )
        ]
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

        return self
