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
import djorm_pgarray.fields as pgarray_fields
from services.accounts import models as account_models
from services.configuration.models import segments as segment_models
from services.configuration.models import tle as tle_models
from services.leop.models import objects as ufo_models


class Launch(django_models.Model):
    """LEOP Cluster database model.
    Database model that manages the information relative to a given leop of
    satellites during the LEOP phases.
    """
    class Meta:
        app_label = 'leop'

    MAX_LEOP_ID_LEN = 30

    admin = django_models.ForeignKey(
        account_models.UserProfile,
        verbose_name='Administrator for this LEOP'
    )

    identifier = django_models.CharField(
        'LEOP identifier',
        max_length=MAX_LEOP_ID_LEN,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex='^[a-zA-Z0-9.\-_]*$',
                message="Alphanumeric or '.-_' required",
                code='invalid_leop_identifier'
            )
        ]
    )

    groundstations = django_models.ManyToManyField(
        segment_models.GroundStation,
        verbose_name='LEOP ground stations'
    )
    ufos = pgarray_fields.SmallIntegerArrayField(
        'Array with the identifiers of the un-identified flying objecs :)'
    )

    date = django_models.DateTimeField(
        'Estimated date and time for the launch'
    )

    cluster_tle = django_models.ForeignKey(
        tle_models.TwoLineElement,
        verbose_name='TLE for the cluster objects as a whole'
    )
    cluster = django_models.ManyToManyField(
        ufo_models.Object,
        verbose_name='Objects for this launch'
    )

    def add_ground_stations(self, identifiers):
        """
        This method adds an existing ground station to the list of registered
        ground stations for this cluster.
        :param identifiers: List with the identifiers of the GroundStations to
                            be added to this cluster.
        """
        for i in identifiers:
            gs = segment_models.GroundStation.objects.get(identifier=i)
            self.groundstations.add(gs)

        self.save()