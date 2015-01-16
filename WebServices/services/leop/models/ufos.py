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
from services.configuration import signals as configuration_signals
from services.configuration.models import segments as segment_models
from services.leop import utils as leop_utils


class UnknownObject(django_models.Model):
    """LEOP database model
    Database model that manages the information relative to an unknown object
    during the LEOP operational phase.
    """
    class Meta:
        app_label = 'leop'

    identifier = django_models.PositiveSmallIntegerField('Object identifier')


class IdentifiedObjectsManager(django_models.Manager):
    """LEOP database manager
    Manages the common opererations with the underlaying IdentifyObjects.
    """
    def create(
        self, admin, launch_id, object_id, callsign, tle_l1, tle_l2, **kwargs
    ):

        tle = leop_utils.create_object_tle(object_id, callsign, tle_l1, tle_l2)
        sc = leop_utils.create_object_spacecraft(
            admin, launch_id, object_id, callsign, tle.identifier
        )

        return super(IdentifiedObjectsManager, self).create(
            identifier=object_id,
            spacecraft=sc,
            **kwargs
        )

    def update(self, launch_id, object_id, callsign, tle_l1, tle_l2):
        """
        Updates the configuration for an identified object with the given data
        :param launch_id: Identifier of the launch
        :param object_id: Identifier for the identified object
        :param callsign: Callsign for the identified object
        :param tle_l1: First line of the TLE for the identified object
        :param tle_l2: Second line of the TLE for the identified object
        :return: Identifier of the object
        """
        ufo = self.get(identifier=object_id)
        if callsign:
            if ufo.spacecraft.callsign != callsign:
                ufo.spacecraft.callsign = callsign
                ufo.spacecraft.save(update_fields=['callsign'])

        if tle_l1 and tle_l2:
            if ufo.spacecraft.tle.first_line != tle_l1 or\
                    ufo.spacecraft.tle.second_line != tle_l2:

                configuration_signals.update_tle_signal.send(
                    sender=ufo,
                    identifier=ufo.spacecraft.tle.identifier,
                    tle_l1=tle_l1,
                    tle_l2=tle_l2
                )

        return ufo.identifier, ufo.spacecraft.identifier

    def delete(self, launch_id, object_id):
        """
        Deletes an identified object from the database together with its
        associated resources (TLE and Spacecraft objects).
        :param launch_id: Identifier of the launch
        :param object_id: Identifier for the identified object
        :return: True if the operation was succesfull
        """
        sc_id = leop_utils.generate_object_sc_identifier(launch_id, object_id)
        sc = segment_models.Spacecraft.objects.get(identifier=sc_id)

        self.get(identifier=object_id).delete()
        sc.tle.delete()
        sc.delete()

        return True


class IdentifiedObject(django_models.Model):
    """LEOP database model
    Database model that manages the information relative to a given identified
    object during the LEOP operational phase.
    """
    class Meta:
        app_label = 'leop'

    objects = IdentifiedObjectsManager()

    identifier = django_models.PositiveSmallIntegerField('Object identifier')
    spacecraft = django_models.ForeignKey(
        segment_models.Spacecraft,
        verbose_name='Spacecraft that represents this object'
    )