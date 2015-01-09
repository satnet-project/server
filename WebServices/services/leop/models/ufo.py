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
        """Manager method.
        Promotes a given UFO object into the <identified> state by associating a
        TLE and alias to it. Basically, it permits detaching this object from
        the cluster and generates the associated GroundTrack for its simulation.
        :param callsign: Alias for the new <identified> object
        :param tle: TLE object created for this UFO
        :param spacecraft: Spacecraft object created for this UFO
        :return: Reference to this "updated" object
        """
        self.callsign = callsign
        self.tle = tle
        self.spacecraft = spacecraft
        self.save()
        return self

    identifier = django_models.PositiveSmallIntegerField(
        'Object sequential identifier'
    )
    callsign = django_models.CharField(
        'Object callsign (future name as a celestrak object?)',
        max_length=30,
        unique=True,
        blank=True,
        validators=[validators.RegexValidator(
            regex='^[a-zA-Z0-9.\-_]*$',
            message="Alphanumeric or '.-_' required",
            code='invalid_leop_identifier'
        )]
    )

    spacecraft = django_models.ForeignKey(
        segment_models.Spacecraft,
        verbose_name='UFO spacecraft for simulation purposes',
        null=True
    )
    tle = django_models.ForeignKey(
        tle_models.TwoLineElement,
        verbose_name='TLE object for simulation purposes',
        null=True
    )