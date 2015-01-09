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
import socket
from services.accounts import models as account_models
from services.configuration.models import segments as segment_models
from services.configuration.models import tle as tle_models
from services.leop.models import ufo as ufo_models


class LEOP(django_models.Model):
    """LEOP Cluster database model.
    Database model that manages the information relative to a given leop of
    satellites during the LEOP phases.
    """
    class Meta:
        app_label = 'leop'

    def add_ufo(self, ufo_id):
        """Database model
        Adds a UFO object to this LEOP cluster by creating it first at the
        related UFO table
        :param ufo_id: The identifier for the UFO object
        :return: The just created UFO object
        """
        with django_db.transaction.atomic():
            ufo = ufo_models.UFO.objects.create(identifier=ufo_id)
            self.cluster.add(ufo)
            self.save()
            return ufo

    def generate_sc_identifier(self, ufo_id, ufo_callsign):
        """Generates SC ID
        Generates the identifier for the simulation-only-purposes spacecraft
        that represents this UFO object.
        :return: String with the identifier
        """
        sc_id = 'leop:' + str(self.identifier) +\
                ':ufo:' + str(ufo_id) +\
                ':cs:' + str(ufo_callsign)
        return sc_id[0:(segment_models.Spacecraft.MAX_SC_ID_LEN - 1)]

    def generate_ufo_tle_source(self, ufo_id, ufo_callsign):
        """UFO TLE Source Generator
        Generates the identificator for the source of the UFO TLE files.
        :param ufo_id: Identifier of the UFO (sequential number)
        :param ufo_callsign: Callsign for the UFO
        :return: String with the complete TLE source
        """
        return 'tle://' + socket.getfqdn() +\
               '/leop/' + str(self.identifier) + '/ufo/' + str(ufo_id)

    def generate_ufo_tle_id(self, ufo_id, ufo_callsign):
        """UFO TLE ID generator
        Generates a complex UFO identifier that is to be used as the initial
        identifier of the associated TLE in the database.
        :param ufo_id: Identifier of the UFO (sequential number)
        :param ufo_callsign: Callsign for the UFO
        :return: String with the complete TLE identifier
        """
        tle_id = 'leop:' + str(self.identifier) +\
                 ':ufo:' + str(ufo_id) +\
                 ':cs:' + str(ufo_callsign)
        return tle_id[0:(tle_models.TwoLineElement.MAX_TLE_ID_LEN - 1)]

    def identify_ufo(self, user, ufo_id, ufo_callsign, tle_l1, tle_l2):
        """UFO identification
        Method that identifies a given ufo from a cluster and associates the
        given TLE to it.
        :param user: User OBJECT that this UFO belongs to
        :param ufo_id: Identifier of the UFO (sequential number)
        :param ufo_callsign: Callsign for the UFO
        :param tle_l1: First line of the UFO's TLE
        :param tle_l2: Second line of the UFO's TLE
        :return: Reference to the UFO object
        """
        ufo = self.cluster.get(identifier=ufo_id)
        tle_id = self.generate_ufo_tle_id(ufo_id, ufo_callsign)
        ufo_tle = tle_models.TwoLineElement.objects.create(
            source=self.generate_ufo_tle_source(ufo_id, ufo_callsign),
            l0=tle_id, l1=tle_l1, l2=tle_l2
        )

        sc_id = self.generate_sc_identifier(ufo_id, ufo_callsign)
        ufo_sc = segment_models.Spacecraft.objects.create(
            tle_id=ufo_tle.identifier,
            user=user,
            identifier=sc_id,
            callsign=ufo_callsign,
            is_ufo=True
        )

        ufo.identify(callsign=ufo_callsign, tle=ufo_tle, spacecraft=ufo_sc)
        return ufo

    def forget_ufo(self, ufo_id):
        """UFO un-identification
        Removes the configuration for the current UFO object and promotes it
        back to a single UFO without callsign or associated TLE/SC pair.
        :param ufo_id: Identifier of the UFO
        :return: Reference to the UFO object
        """
        ufo = self.cluster.get(identifier=ufo_id)
        #print '>>> ufo = ' + str(ufo.identifier) +\
        #      ', spacecraft = ' + str(ufo.spacecraft.identifier)
        # TODO: Review problem of accessing <ufo.spacecraft.delete>
        x = ufo.spacecraft.identifier
        ufo.tle.delete()
        ufo.spacecraft.delete()
        ufo.callsign = ''
        ufo.save()
        return ufo

    admin = django_models.ForeignKey(
        account_models.UserProfile,
        verbose_name='Administrator for this LEOP'
    )

    identifier = django_models.CharField(
        'LEOP identifier',
        max_length=30,
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

    cluster_tle = django_models.ForeignKey(
        tle_models.TwoLineElement,
        verbose_name='TLE for the cluster objects as a whole',
        null=True
    )
    cluster = django_models.ManyToManyField(
        ufo_models.UFO,
        verbose_name='UFO Objects'
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