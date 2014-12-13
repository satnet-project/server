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
from django.db import models
from services.accounts import models as account_models
from services.configuration.models import segments as segment_models


class ClusterManager(models.Manager):
    """Cluster database mdoel manager.
    Model manager for the database Cluster model.
    """
    pass


class Cluster(models.Model):
    """Cluster database model.
    Database model that manages the information relative to a given leop
    of satellites during the LEOP phases.
    """

    class Meta:
        app_label = 'leop'

    objects = ClusterManager()

    admin = models.ForeignKey(
        account_models.UserProfile, verbose_name='Cluster administrator'
    )

    identifier = models.CharField(
        'Cluster identifier',
        max_length=30,
        unique=True,
        validators=[validators.RegexValidator(
            regex='^[a-zA-Z0-9.\-_]*$',
            message="Alphanumeric or '.-_' required",
            code='invalid_cluster_identifier'
        )]
    )

    groundstations = models.ManyToManyField(
        segment_models.GroundStation, verbose_name='Cluster ground stations',
    )
    spacecraft = models.ManyToManyField(
        segment_models.Spacecraft, verbose_name='Cluster spacecraft'
    )