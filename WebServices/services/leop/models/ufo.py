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


class UFO(segment_models.Spacecraft):
    """UFO database model.
    Database model that manages the information relative to a spacecraft that
    has not being identified completely yet.
    """
    class Meta:
        app_label = 'leop'

    def identify(self, callsign, tle, spacecraft):
        """Object method
        Promotes a given UFO object into the <identified> state by associating a
        TLE and callsign to it. Basically, it permits detaching this object from
        the cluster and generates the associated GroundTrack for its simulation.
        :param callsign: Alias for the new <identified> object
        :param tle: TLE object created for this UFO
        :param spacecraft: Spacecraft object created for this UFO
        :return: Reference to this "updated" object
        """
        self.callsign = callsign
        self.tle = tle
        self.spacecraft = spacecraft
        self.is_identified = True
        self.save()
        return self

    def forget(self):
        """Object method
        Forgets the configuration for this UFO and transforms it in an unknow.
        :return: Reference to this object
        """
        if not self.is_identified:
            raise Exception('UFO object has not been identified yet')

        self.callsign = ''
        self.tle.delete()
        self.spacecraft.delete()
        self.is_identified = False
        self.save()

        return self

    def update(
        self, callsign=None, tle_id=None, tle_l1=None, tle_l2=None, **kwargs
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

        if tle_id and self.tle.identifier != tle_id:
            return super(UFO, self).update(callsign=callsign, tle_id=tle_id)

        # TLE dirty check
        if (self.tle.first_line != tle_l1) or (self.tle.second_line != tle_l2):

            self.tle.first_line = tle_l1
            self.tle.second_line = tle_l2
            self.tle.save(update_fields=['first_line', 'second_line'])

        return self

    is_identified = django_models.BooleanField(
        'Flag that indicates whether this UFO has been identified or not',
        default=False
    )