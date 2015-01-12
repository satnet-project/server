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


def generate_object_sc_identifier(launch_id, object_id):
    """Helper method
    Generates the identifier for the simulation-only-purposes spacecraft
    that represents this UFO object.
    :param launch_id: Identifier of the launch
    :param object_id: Identifier of the UFO (sequential number)
    :return: String with the complete TLE source
    """
    sc_id = 'sc:' + str(launch_id) + ':' + str(object_id)
    return sc_id[0:(segment_models.Spacecraft.MAX_SC_ID_LEN - 1)]


def generate_object_tle_source(object_id):
    """Helper method
    Generates the identificator for the source of the UFO TLE files.
    :param object_id: Identifier of the UFO (sequential number)
    :return: String with the complete TLE source
    """
    return 'https://' + socket.getfqdn() + '/ufo/' + str(object_id)


def generate_object_tle_id(object_id, callsign):
    """Helper method
    Generates a complex UFO identifier that is to be used as the initial
    identifier of the associated TLE in the database.
    :param object_id: Identifier of the UFO (sequential number)
    :param callsign: Callsign for the UFO
    :return: String with the complete TLE source
    """
    tle_id = 'ufo:' + str(object_id) + ':cs:' + str(callsign)
    return tle_id[0:(tle_models.TwoLineElement.MAX_TLE_ID_LEN - 1)]


def create_object_tle(object_id, callsign, tle_l1, tle_l2):
    """Helper method
    Creates a TLE for this UFO object.
    :param object_id: Identifier of the UFO object
    :param callsign: Callsign for the UFO
    :param tle_l1: First line of the UFO's TLE
    :param tle_l2: Second line of the UFO's TLE
    :return: Reference to the just-created object
    """
    tle_source = generate_object_tle_source(object_id)
    tle_id = generate_object_tle_id(object_id, callsign)
    return tle_models.TwoLineElement.objects.create(
        source=tle_source, l0=tle_id, l1=tle_l1, l2=tle_l2
    )


def create_object_spacecraft(
    user_profile, launch_id, object_id, callsign, tle_id
):
    """Helper method
    Creates the spacecraft that simulates the position of this object.
    :param object_id: Identifier of the object
    :param tle_id: Identifier of the TLE
    :return: Reference to the just created spacecraft object
    """
    sc_id = generate_object_sc_identifier(
        launch_id, object_id, callsign
    )

    return segment_models.Spacecraft.objects.create(
        user=user_profile,
        identifier=sc_id,
        callsign=callsign,
        tle_id=tle_id,
        is_cluster=True
    )


def generate_cluster_tle_source(launch_id):
    """Helper method
    Generates the identificator for the source of the cluster TLE files.
    :param launch_id: Identifier of the UFO (sequential number)
    :return: String with the complete TLE source
    """
    return 'https://' + socket.getfqdn() + '/cluster/' + str(launch_id)


def generate_cluster_tle_id(launcher_id):
    """Helper method
    Generates a complex UFO identifier that is to be used as the initial
    identifier of the associated TLE in the database.
    :param launcher_id: Identifier of the UFO (sequential number)
    :return: String with the complete TLE source
    """
    tle_id = 'cluster:' + str(launcher_id)
    return tle_id[0:(tle_models.TwoLineElement.MAX_TLE_ID_LEN - 1)]


def create_cluster_tle(launch_id, tle_l1, tle_l2):
    """Helper method
    Creates a TLE for this UFO object.
    :param launch_id: Identifier of the UFO object
    :param tle_l1: First line of the UFO's TLE
    :param tle_l2: Second line of the UFO's TLE
    :return: Reference to the just-created object
    """
    tle_source = generate_cluster_tle_source(launch_id)
    tle_id = generate_cluster_tle_id(launch_id)
    return tle_models.TwoLineElement.objects.create(
        source=tle_source, l0=tle_id, l1=tle_l1, l2=tle_l2
    )


def generate_cluster_sc_identifier(launch_id, callsign):
    """Helper method
    Generates the identifier for the simulation-only-purposes spacecraft
    that represents this UFO object.
    :param launch_id: Identifier of the UFO (sequential number)
    :param callsign: Callsign for the UFO
    :return: String with the complete TLE source
    """
    sc_id = 'cluster:' + str(launch_id) + ':cs:' + str(callsign)
    return sc_id[0:(segment_models.Spacecraft.MAX_SC_ID_LEN - 1)]


def generate_cluster_callsign(launch_id):
    """Helper method
    Generates the identifier for the simulation-only-purposes spacecraft
    that represents this cluster object.
    :param launch_id: Identifier of the cluster
    :return: String with the identifier
    """
    sc_id = 'cluster:' + str(launch_id) + ':cs'
    return sc_id[0:(segment_models.Spacecraft.MAX_CALLSIGN_LEN - 1)]


def create_cluster_spacecraft(user_profile, launch_id, tle_id):
    """Helper method
    :param launch_id:
    :param tle_id:
    :return: Reference to the just created spacecraft object
    """
    sc_callsign = generate_cluster_callsign(launch_id)
    sc_id = generate_cluster_sc_identifier(launch_id, sc_callsign)

    return segment_models.Spacecraft.objects.create(
        user=user_profile,
        identifier=sc_id,
        callsign=sc_callsign,
        tle_id=tle_id,
        is_cluster=True
    )