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
import logging
from services.accounts import models as account_models
from services.configuration.models import segments as segment_models
from services.configuration.models import tle as tle_models
from services.leop import utils as leop_utils

logger = logging.getLogger('leop')


class LaunchManager(django_models.Manager):
    """Database manager
    Custom manager for the Launch objects within the database.
    """

    def add_ground_stations(self, identifier, groundstations):
        """
        This method adds an existing ground station to the list of registered
        ground stations for this cluster.
        :param identifier: Identifier of the launch object
        :param groundstations: List with the identifiers of the GroundStations
                                to be added to this cluster
        :return: Identifier of the launch object
        """
        launch = self.get(identifier=identifier)

        for i in groundstations:
            gs = segment_models.GroundStation.objects.get(identifier=i)
            launch.groundstations.add(gs)

        launch.save()

        return identifier

    def remove_groundstations(self, identifier, groundstations):
        """
        This method removes the ground stations given as a parameter from the
        list of groundstations registered as part of this launch.
        :param identifier: Identifier of the launch
        :param groundstations: List of groundstations to be removed
        :return: True if the operation was succesful
        """
        launch = self.get(identifier=identifier)

        for g_id in groundstations:

            g = launch.groundstations.get(identifier=g_id)
            launch.groundstations.remove(g)

        launch.save()

        return True

    def add_unknown(self, identifier, object_identifier):
        """
        Adds a new unknown object to the list.
        :param identifier: Identifier of the launch object
        :param object_identifier: Numerical identifier of the unknown object
        :return: Identifier of the created unknown object (int)
        """
        launch = self.get(identifier=identifier)

        if object_identifier < 0:
            raise Exception('Identifier has to be > 0')

        unknown = launch.unknown_objects
        if object_identifier in unknown:
            raise Exception('UFO already exists, id = ' + str(id))

        launch.unknown_objects = unknown + [object_identifier]
        launch.save()

        return object_identifier

    def remove_unknown(self, identifier, object_identifier):
        """
        Removes the given identifier from the list.
        :param identifier: Identifier of the launch object
        :param object_identifier: Numerical (int) identifier to be removed
        :return: True if the operation was succesful
        """
        launch = self.get(identifier=identifier)

        if object_identifier < 0:
            raise Exception('Identifier has to be > 0')

        u_objects = launch.unknown_objects
        if not object_identifier in u_objects:
            raise Exception('Identifier not found')

        launch.unknown_objects = u_objects.remove(object_identifier)
        launch.save()

        return True

    def create(
        self, admin=None, identifier=None, tle_l1=None, tle_l2=None,
        **kwargs
    ):
        """Custom create method
        Custom create method that creates the TLE for this launch and
        initializes the list of unknown objects to an empty one.
        :param admin: Username of the owner of this launch object
        :param identifier: Identifier of the launcher
        :param tle_l1: First line of the TLE for the cluster
        :param tle_l2: Second line of the TLE for the cluster
        :param kwargs: All other parameters
        :return: Reference to the just created Launch object
        """
        logger.info('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        print '###########################################'
        print '###########################################'
        print 'XXXX'

        #tle = leop_utils.create_cluster_tle(identifier, tle_l1, tle_l2)
        print '###########################################'
        print '###########################################'
        #print '>>> tle.id = ' + str(tle.identifier)

        #spacecraft = leop_utils.create_cluster_spacecraft(
        #    user_profile=admin,
        #    launch_identifier=identifier,
        #    tle_id=tle.identifier
        #)

        print '###########################################'
        print '###########################################'
        #print '>>> spacecraft.id = ' + str(spacecraft.identifier)

        return super(LaunchManager, self).create(
            admin=admin,
            identifier=identifier,
            tle=None,
            spacecraft=None,
            unknown_objects=[],
            **kwargs
        )


class Launch(django_models.Model):
    """LEOP Cluster database model.
    Database model that manages the information relative to a given leop of
    satellites during the LEOP phases.
    """
    class Meta:
        app_label = 'leop'

    objects = LaunchManager()

    MAX_LAUNCH_ID_LEN = 30

    admin = django_models.ForeignKey(
        account_models.UserProfile,
        verbose_name='Administrator for this LEOP'
    )

    identifier = django_models.CharField(
        'LEOP identifier',
        max_length=MAX_LAUNCH_ID_LEN,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex='^[a-zA-Z0-9.\-_]*$',
                message="Alphanumeric or '.-_' required",
                code='invalid_leop_identifier'
            )
        ]
    )

    date = django_models.DateTimeField('Launch date')

    groundstations = django_models.ManyToManyField(
        segment_models.GroundStation,
        verbose_name='LEOP ground stations'
    )

    tle = django_models.ForeignKey(
        tle_models.TwoLineElement,
        verbose_name='TLE for the cluster of objects as a whole'
    )
    spacecraft = django_models.ForeignKey(
        segment_models.Spacecraft,
        verbose_name='Spacecraft that represents the whole cluster',
        related_name='cluster'
    )

    unknown_objects = pgarray_fields.SmallIntegerArrayField(
        'Array with the identifiers of the un-identified flying objecs :)'
    )
    identified_objects = django_models.ManyToManyField(
        segment_models.Spacecraft,
        verbose_name='Spacecraft identified from within the cluster'
    )