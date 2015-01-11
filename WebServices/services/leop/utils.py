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

import socket
from services.configuration.models import segments as segment_models
from services.configuration.models import tle as tle_models


def generate_object_sc_identifier(identifier, callsign):
    """Helper method
    Generates the identifier for the simulation-only-purposes spacecraft
    that represents this UFO object.
    :param identifier: Identifier of the UFO (sequential number)
    :param callsign: Callsign for the UFO
    :return: String with the complete TLE source
    """
    sc_id = 'ufo:' + str(identifier) + ':cs:' + str(callsign)
    return sc_id[0:(segment_models.Spacecraft.MAX_SC_ID_LEN - 1)]


def generate_object_tle_source(identifier):
    """Helper method
    Generates the identificator for the source of the UFO TLE files.
    :param identifier: Identifier of the UFO (sequential number)
    :return: String with the complete TLE source
    """
    return 'https://' + socket.getfqdn() + '/ufo/' + str(identifier)


def generate_object_tle_id(identifier, callsign):
    """Helper method
    Generates a complex UFO identifier that is to be used as the initial
    identifier of the associated TLE in the database.
    :param identifier: Identifier of the UFO (sequential number)
    :param callsign: Callsign for the UFO
    :return: String with the complete TLE source
    """
    tle_id = 'ufo:' + str(identifier) + ':cs:' + str(callsign)
    return tle_id[0:(tle_models.TwoLineElement.MAX_TLE_ID_LEN - 1)]


def create_object_tle(identifier, callsign, tle_l1, tle_l2):
    """Helper method
    Creates a TLE for this UFO object.
    :param identifier: Identifier of the UFO object
    :param callsign: Callsign for the UFO
    :param tle_l1: First line of the UFO's TLE
    :param tle_l2: Second line of the UFO's TLE
    :return: Reference to the just-created object
    """
    tle_source = generate_object_tle_source(identifier)
    tle_id = generate_object_tle_id(identifier, callsign)
    return tle_models.TwoLineElement.objects.create(
        source=tle_source, l0=tle_id, l1=tle_l1, l2=tle_l2
    )


def generate_cluster_tle_source(identifier):
    """Helper method
    Generates the identificator for the source of the cluster TLE files.
    :param identifier: Identifier of the UFO (sequential number)
    :return: String with the complete TLE source
    """
    return 'https://' + socket.getfqdn() + '/cluster/' + str(identifier)


def generate_cluster_tle_id(identifier):
    """Helper method
    Generates a complex UFO identifier that is to be used as the initial
    identifier of the associated TLE in the database.
    :param identifier: Identifier of the UFO (sequential number)
    :return: String with the complete TLE source
    """
    tle_id = 'cluster:' + str(identifier)
    return tle_id[0:(tle_models.TwoLineElement.MAX_TLE_ID_LEN - 1)]


def create_cluster_tle(identifier, tle_l1, tle_l2):
    """Helper method
    Creates a TLE for this UFO object.
    :param identifier: Identifier of the UFO object
    :param tle_l1: First line of the UFO's TLE
    :param tle_l2: Second line of the UFO's TLE
    :return: Reference to the just-created object
    """
    tle_source = generate_cluster_tle_source(identifier)
    tle_id = generate_cluster_tle_id(identifier)
    return tle_models.TwoLineElement.objects.create(
        source=tle_source, l0=tle_id, l1=tle_l1, l2=tle_l2
    )


def generate_cluster_sc_identifier(identifier, callsign):
    """Helper method
    Generates the identifier for the simulation-only-purposes spacecraft
    that represents this UFO object.
    :param identifier: Identifier of the UFO (sequential number)
    :param callsign: Callsign for the UFO
    :return: String with the complete TLE source
    """
    sc_id = 'cluster:' + str(identifier) + ':cs:' + str(callsign)
    return sc_id[0:(segment_models.Spacecraft.MAX_SC_ID_LEN - 1)]


def generate_cluster_callsign(identifier):
    """Helper method
    Generates the identifier for the simulation-only-purposes spacecraft
    that represents this cluster object.
    :param identifier: Identifier of the cluster
    :return: String with the identifier
    """
    sc_id = 'cluster:' + str(identifier) + ':cs'
    return sc_id[0:(segment_models.Spacecraft.MAX_CALLSIGN_LEN - 1)]


def create_cluster_spacecraft(user_profile, launch_identifier, tle_id):
    """Helper method
    :param launch_identifier:
    :param tle_id:
    :return: Reference to the just created spacecraft object
    """
    sc_callsign = generate_cluster_callsign(launch_identifier)
    sc_id = generate_cluster_sc_identifier(launch_identifier, sc_callsign)

    return segment_models.Spacecraft.objects.create(
        user=user_profile,
        identifier=sc_id,
        callsign=sc_callsign,
        tle_id=tle_id,
        is_cluster=True
    )