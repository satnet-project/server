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
from services.configuration.models import tle as tle_models


class UFOManager(django_models.Manager):
    """UFO database manager.
    Manager for helping in handling ufo objects.
    """
    class Meta:
        app_label = 'leop'

    def add(self, identifier, tle):
        pass


class UFO(django_models.Model):
    """UFO database model.
    Database model that manages the information relative to a spacecraft that
    has not being identified completely yet.
    """
    class Meta:
        app_label = 'leop'

    identifier = django_models.CharField(
        'LEOP identifier',
        max_length=30,
        unique=True,
        validators=[validators.RegexValidator(
            regex='^[a-zA-Z0-9.\-_]*$',
            message="Alphanumeric or '.-_' required",
            code='invalid_leop_identifier'
        )]
    )
    alias = django_models.CharField(
        'LEOP alias',
        max_length=30,
        unique=True,
        validators=[validators.RegexValidator(
            regex='^[a-zA-Z0-9.\-_]*$',
            message="Alphanumeric or '.-_' required",
            code='invalid_leop_identifier'
        )]
    )

    tle = django_models.ForeignKey(
        tle_models.TwoLineElement,
        verbose_name='TLE for this UFO object',
        blank=True
    )