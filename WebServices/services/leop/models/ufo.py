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

from django.core import validators
from django import db as django_db
from django.db import models as django_models
from services.configuration.models import segments as segment_models
from services.configuration.models import tle as tle_models


class UFO(django_models.Model):
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
        with django_db.transaction.atomic():
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
        with django_db.transaction.atomic():

            self.callsign = ''
            self.tle.delete()
            self.spacecraft.delete()
            self.is_identified = False

            self.save()
            return self

    def update(self, callsign, tle_l1, tle_l2):
        """Object method
        Updates the configuration for this UFO object.
        :param callsign: Callsign for the UFO
        :param tle_l1: First line of the UFO's TLE
        :param tle_l2: Second line of the UFO's TLE
        :return: Reference to this object
        """
        with django_db.transaction.atomic():

            # Callsign dirty check
            if self.callsign != callsign:
                self.callsign = callsign
                self.save()

            # TLE dirty check
            if (self.tle.first_line != tle_l1) or (
                self.tle.second_line != tle_l2
            ):

                self.tle.first_line = tle_l1
                self.tle.second_line = tle_l2
                self.tle.save(update_fields=['first_line', 'second_line'])

            self.spacecraft.update(callsign, self.tle.identifier)

            return self

    identifier = django_models.PositiveSmallIntegerField(
        'Object sequential identifier'
    )
    callsign = django_models.CharField(
        'Object callsign (future name as a celestrak object?)',
        max_length=30,
        blank=True,
        validators=[validators.RegexValidator(
            regex='^[a-zA-Z0-9.\-_]*$',
            message="Alphanumeric or '.-_' required",
            code='invalid_leop_identifier'
        )]
    )
    is_identified = django_models.BooleanField(
        'Flag that indicates whether this UFO has been identified or not',
        default=False
    )

    spacecraft = django_models.ForeignKey(
        segment_models.Spacecraft,
        verbose_name='UFO spacecraft for simulation purposes',
        on_delete=django_models.SET_NULL,
        null=True
    )
    tle = django_models.ForeignKey(
        tle_models.TwoLineElement,
        verbose_name='TLE object for simulation purposes',
        on_delete=django_models.SET_NULL,
        null=True
    )