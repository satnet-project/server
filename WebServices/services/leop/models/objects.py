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

from django.db import models as django_models
from services.configuration.models import segments as segment_models


class ObjectManager(django_models.Manager):
    """UFO database manager
    Custom manager for the UFO objects.
    """

    def create(self, identifier, callsign, tle_l1, tle_l2, **kwargs):
        """
        Creates a new UFO object in the database initializing the parent
        spacecraft.
        :param identifier: Identifier of the UFO object
        :param callsign: Callsign for the UFO
        :param tle_l1: First line of the UFO's TLE
        :param tle_l2: Second line of the UFO's TLE
        :param kwargs: Dictionary with additional parameters
        :return: Reference to the just-created object
        """
        sc_id = ObjectManager.generate_sc_identifier(
            identifier=identifier, callsign=callsign
        )
        tle = ObjectManager.create_ufo_tle(
            identifier=identifier, callsign=callsign,
            tle_l1=tle_l1, tle_l2=tle_l2
        )
        return super(ObjectManager, self).create(
            tle_id=tle.identifier, identifier=sc_id, is_ufo=True
        )


class Object(segment_models.Spacecraft):
    """UFO database model
    Database model that manages the information relative to a spacecraft that
    has not being identified completely yet.
    """
    class Meta:
        app_label = 'leop'

    objects = ObjectManager()

    is_identified = django_models.BooleanField(
        'Flag that indicates whether this UFO has been identified or not',
        default=True
    )

    def identify(self, callsign, tle_l1, tle_l2):
        """Object method
        Identifies this object setting a configuration for the same.
        :param callsign: Callsign for the UFO
        :param tle_l1: First line of the UFO's TLE
        :param tle_l2: Second line of the UFO's TLE
        :return: Reference to this object
        """
        if self.is_identified:
            raise Exception('UFO object has not been identified yet')

        tle = ObjectManager.create_ufo_tle(
            identifier=self.identifier, callsign=callsign,
            tle_l1=tle_l1, tle_l2=tle_l2
        )
        return self.update(
            callsign=callsign, tle_l1=tle_l1, tle_l2=tle_l2,
            is_identified=True
        )

    def forget(self):
        """Object method
        Forgets the configuration for this UFO and transforms it in an unknow.
        :return: Reference to this object
        """
        if not self.is_identified:
            raise Exception('UFO object has not been identified yet')

        self.tle.delete()
        self.callsign = ''
        self.is_identified = False
        self.save()

        return self

    def update(
        self,
        callsign=None, tle_l1=None, tle_l2=None, is_identified=False,
        **kwargs
    ):
        """Object method
        Updates the configuration for this UFO object.
        :param callsign: Callsign for the UFO
        :param tle_l1: First line of the UFO's TLE
        :param tle_l2: Second line of the UFO's TLE
        :return: Reference to this object
        """
        # Callsign dirty check
        if self.callsign != callsign:
            self.callsign = callsign
            self.save()

        # TLE dirty check
        if (self.tle.first_line != tle_l1) or (self.tle.second_line != tle_l2):

            self.tle.first_line = tle_l1
            self.tle.second_line = tle_l2
            self.tle.save()

        return self