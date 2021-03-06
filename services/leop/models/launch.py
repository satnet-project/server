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
import logging
from services.accounts import models as account_models
from services.configuration.models import segments as segment_models
from services.configuration.models import tle as tle_models
from services.configuration.signals import tle as cfg_tle_signals
from services.leop import push as leop_push
from services.leop import utils as leop_utils
from services.leop.models import ufos as ufo_models

logger = logging.getLogger('leop')


class LaunchManager(django_models.Manager):
    """Database manager
    Custom manager for the Launch objects within the database.
    """

    def add_ground_stations(self, launch_id, groundstations):
        """
        This method adds an existing ground station to the list of registered
        ground stations for this cluster.
        :param launch_id: Identifier of the launch object
        :param groundstations: List with the identifiers of the GroundStations
                                to be added to this cluster
        :return: Identifier of the launch object
        """
        launch = self.get(identifier=launch_id)

        for i in groundstations:

            gs = segment_models.GroundStation.objects.get(identifier=i)
            launch.groundstations.add(gs)

        launch.save()

        return launch_id

    def remove_groundstations(self, launch_id, groundstations):
        """
        This method removes the ground stations given as a parameter from the
        list of groundstations registered as part of this launch.
        :param launch_id: Identifier of the launch
        :param groundstations: List of groundstations to be removed
        :return: True if the operation was succesful
        """
        launch = self.get(identifier=launch_id)

        for g_id in groundstations:

            g = launch.groundstations.get(identifier=g_id)
            launch.groundstations.remove(g)

        launch.save()
        return True

    def add_unknown(self, launch_id, object_id):
        """
        Adds a new unknown object to the list.
        :param launch_id: Identifier of the launch object
        :param object_id: Numerical identifier of the unknown object
        :return: Identifier of the created unknown object (int)
        """
        return self.get(identifier=launch_id).add_unknown(object_id)

    def remove_unknown(self, launch_id, object_id):
        """
        Removes the given identifier from the list.
        :param launch_id: Identifier of the launch object
        :param object_id: Numerical (int) identifier to be removed
        :return: True if the operation was succesful
        """
        return self.get(identifier=launch_id).remove_unknown(object_id)

    def update_identified(self, launch_id, object_id, callsign, tle_l1, tle_l2):
        """
        Updates the configuration for an identified object with the given data
        :param launch_id: Identifier of the launch
        :param object_id: Identifier for the identified object
        :param callsign: Callsign for the identified object
        :param tle_l1: First line of the TLE for the identified object
        :param tle_l2: Second line of the TLE for the identified object
        :return: Identifier of the object
        """
        return self.get(identifier=launch_id).update_identified(
            launch_id, object_id, callsign, tle_l1, tle_l2
        )

    def identify(self, launch_id, object_id, callsign, tle_l1, tle_l2):
        """Manager method
        Promotes an unidentified object into an identified one.
        :param launch_id: Launch identifier
        :param object_id: Identifier of the object to be promoted
        :param callsign: Callsign for the identified object
        :param tle_l1: First line of the TLE for the new identified object
        :param tle_l2: Second line of the TLE for the new identified object
        :return:
        """
        launch = self.get(identifier=launch_id)
        identified = launch.add_identified(
            launch.admin, launch_id, object_id, callsign, tle_l1, tle_l2
        )
        launch.remove_unknown(object_id)
        return identified

    def forget(self, launch_id, object_id):
        """Manager method
        Moves an identified object back to the unknown objects list and removes
        all allocated resources.
        :param launch_id: Launch identifier
        :param object_id: Identifier of the object to be promoted
        :return: True if the operation was succesful
        """
        launch = self.get(identifier=launch_id)
        launch.remove_identified(launch_id, object_id)
        launch.add_unknown(object_id)
        return True

    def create(
        self, admin, launch_id, date, tle_l1, tle_l2, **kwargs
    ):
        """Custom create method
        Custom create method that creates the TLE for this launch and
        initializes the list of unknown objects to an empty one.
        :param admin: Username of the owner of this launch object
        :param launch_id: Identifier of the launcher
        :param date: Date of the launch
        :param tle_l1: First line of the TLE for the cluster
        :param tle_l2: Second line of the TLE for the cluster
        :param kwargs: All other parameters
        :return: Reference to the just created Launch object
        """
        if not admin:
            raise Exception('No admin provided')
        if not date:
            raise Exception('No date provided')

        tle = leop_utils.create_cluster_tle(launch_id, tle_l1, tle_l2)
        spacecraft = leop_utils.create_cluster_spacecraft(
            user_profile=admin,
            launch_id=launch_id,
            tle_id=tle.identifier
        )

        return super(LaunchManager, self).create(
            admin=admin,
            identifier=launch_id,
            tle=tle,
            cluster_spacecraft_id=spacecraft.identifier,
            date=date,
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

    cluster_spacecraft_id = django_models.CharField(
        'Cluster spacecraft identifier',
        unique=True,
        max_length=segment_models.Spacecraft.MAX_SC_ID_LEN,
        validators=[validators.RegexValidator(
            regex='^[a-zA-Z0-9.\-_]*$',
            message="Alphanumeric or '.-_' required",
            code='invalid_spacecraft_identifier'
        )]
    )

    tle = django_models.ForeignKey(
        tle_models.TwoLineElement,
        verbose_name='TLE for the cluster of objects as a whole'
    )

    unknown_objects = django_models.ManyToManyField(
        ufo_models.UnknownObject,
        verbose_name='Objects still unknown'
    )
    identified_objects = django_models.ManyToManyField(
        ufo_models.IdentifiedObject,
        verbose_name='Object identified from within the cluster'
    )

    def add_unknown(self, object_id):
        """Object method
        Adds a new unknown object to this launch object.
        :param object_id: Identifier for the unknown object
        :return: Identifier of the object
        """
        if object_id < 0:
            raise Exception('Identifier has to be > 0')
        if self.unknown_objects.filter(identifier=object_id).exists():
            raise Exception('Unknown object already exists, id = ' + str(id))

        self.unknown_objects.create(identifier=object_id)
        self.save()

        return object_id

    def remove_unknown(self, object_id):
        """Object method
        Removes a given unknown object from this launch object.
        :param object_id: Identifier for the unknown object
        :return: True if the operation was succesfull
        """
        if object_id < 0:
            raise Exception('Identifier has to be > 0')
        if not self.unknown_objects.filter(identifier=object_id).exists():
            raise Exception('Unknown object does not exist, id = ' + str(id))

        self.unknown_objects.get(identifier=object_id).delete()
        self.save()

        return True

    def add_identified(
        self, admin, launch_id, object_id, callsign, tle_l1, tle_l2
    ):
        """
        Adds an identified objectd to the list of identified ones.
        :param admin: owner of the associated spacecraft object
        :param launch_id: Identifier of the launch
        :param object_id: Identifier for the identified object
        :param callsign: Callsign for the identified object
        :param tle_l1: First line of the TLE for the identified object
        :param tle_l2: Second line of the TLE for the identified object
        :return: (object_id, spacecraft_id)
        """
        if object_id < 0:
            raise Exception('Identifier has to be > 0')
        if self.identified_objects.filter(identifier=object_id).exists():
            raise Exception('Identified object already exists, id = ' + str(id))

        identified = ufo_models.IdentifiedObject.objects.create(
            admin, launch_id, object_id, callsign, tle_l1, tle_l2
        )

        self.identified_objects.add(identified)
        self.save()

        return object_id, identified.spacecraft.identifier

    def update_identified(self, launch_id, object_id, callsign, tle_l1, tle_l2):
        """
        Updates the configuration for an identified object with the given data
        :param launch_id: Identifier of the launch
        :param object_id: Identifier for the identified object
        :param callsign: Callsign for the identified object
        :param tle_l1: First line of the TLE for the identified object
        :param tle_l2: Second line of the TLE for the identified object
        :return: Identifier of the object
        """
        if object_id < 0:
            raise Exception('Identifier has to be > 0')
        if not self.identified_objects.filter(identifier=object_id).exists():
            raise Exception(
                'Identified object (sc) does not exist, id = ' + str(object_id)
            )
        return ufo_models.IdentifiedObject.objects.update(
            launch_id, object_id, callsign, tle_l1, tle_l2
        )

    def remove_identified(self, launch_id, object_id):
        """
        Removes an identified object from the list together with the associated
        resources.
        :param launch_id: Identifier of the launch
        :param object_id: Identifier for the identified object
        :return: True if the operation was succesfull
        """
        if object_id < 0:
            raise Exception('Identifier has to be > 0')
        if not self.identified_objects.filter(identifier=object_id).exists():
            raise Exception(
                'Identified object (sc) does not exist, id = ' + str(object_id)
            )

        ufo_models.IdentifiedObject.objects.delete(launch_id, object_id)

        self.save()
        return True

    def update(self, date=None, tle_l1=None, tle_l2=None):
        """Model method
        Updates the configuration of this object by performing a dirty check
        in between the new values and the ones stored in the database.
        :param date: The new date object
        :param tle_l1: The first line of the new TLE
        :param tle_l2: The second line of the new TLE
        :return: Launch object's identifier
        """
        if date:
            if self.date != date:
                self.date = date
                self.save(update_fields=['date'])

        if tle_l1 and tle_l2:
            if self.tle.first_line != tle_l1 or self.tle.second_line != tle_l2:

                leop_push.LaunchPush.trigger_leop_sc_updated(
                    self.identifier, self.cluster_spacecraft_id
                )

                cfg_tle_signals.update_tle_signal.send(
                    sender=self, identifier=self.tle.identifier,
                    tle_l1=tle_l1, tle_l2=tle_l2
                )

        return self.identifier
