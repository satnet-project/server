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

import rpc4django
from django.core import exceptions as django_ex
from services.configuration.models import segments as segment_models
from services.leop.models import launch as launch_models
from services.leop.jrpc.serializers import launch as launch_serial


@rpc4django.rpcmethod(
    name='leop.gs.list',
    signature=['String'],
    login_required=True
)
def list_groundstations(launch_id, **kwargs):
    """JRPC method (LEOP service).
    Returns the list of groundstations available for creating this LEOP
    system. In case a Ground Station is already in use for this system, it will
    not be listed.
    :param launch_id: Identifier of the LEOP cluster.
    :param kwargs: Dictionary with additional variables like the HTTP request
                    itself (defined by RPC4Django).
    :return: List of the identifiers of the available groundstations.
    """

    # user must be obtained from the request, since this has already been
    # validated by the authentication backend
    http_request = kwargs.get('request', None)
    if not http_request or not http_request.user.is_staff:
        raise django_ex.PermissionDenied()

    leop_cluster = launch_models.Launch.objects.get(identifier=launch_id)

    # List construction: ground stations in use and available for LEOP
    u_gs = leop_cluster.groundstations.all()
    all_gs = segment_models.GroundStation.objects.all()
    a_gs = [item for item in all_gs if item not in u_gs]

    # Serialization to a JSON-RPC-like object
    return launch_serial.serialize_gs_lists(a_gs, u_gs)


@rpc4django.rpcmethod(
    name='leop.gs.add',
    signature=['String', 'Object'],
    login_required=True
)
def add_groundstations(launch_id, groundstations, **kwargs):
    """JRPC method (LEOP service).
    Adds the array of GroundStations to the LEOP cluster. If any of the given
    GroundStation identifiers does not exist, the operation is cancelled and
    an 'ObjectDoesNotExist' exception is raised.
    :param launch_id: Identifier of the LEOP cluster
    :param groundstations: List with the GroundStations to be added
    :return: Identifier of the just-updated LEOP cluster
    """
    # user must be obtained from the request, since this has already been
    # validated by the authentication backend
    http_request = kwargs.get('request', None)
    if not http_request or not http_request.user.is_staff:
        raise django_ex.PermissionDenied()
    if not groundstations:
        raise Exception('No groundstations provided')

    # Serialization to a JSON-RPC-like object
    return launch_serial.serialize_leop_id(
        launch_models.Launch.objects.add_ground_stations(
            launch_id, groundstations
        )
    )


@rpc4django.rpcmethod(
    name='leop.gs.remove',
    signature=['String', 'Object'],
    login_required=True
)
def remove_groundstations(launch_id, groundstations, **kwargs):
    """JRPC method (LEOP service).
    Removes the array of GroundStations from the LEOP cluster. If any of the
    given GroundStation identifiers does not exist, the operation is
    cancelled and an 'ObjectDoesNotExist' exception is raised.
    :param launch_id: Identifier of the LEOP cluster.
    :param groundstations: List with the GroundStations to be added.
    :return: True if the operation was succesfully completed
    """
    # user must be obtained from the request, since this has already been
    # validated by the authentication backend
    http_request = kwargs.get('request', None)
    if not http_request or not http_request.user.is_staff:
        raise django_ex.PermissionDenied()
    if not groundstations:
        return launch_serial.serialize_leop_id(launch_id)

    # Serialization to a JSON-RPC-like object
    return launch_models.Launch.objects.remove_groundstations(
        launch_id, groundstations
    )


@rpc4django.rpcmethod(
    name='leop.launch.addUnknown',
    signature=['String', 'int'],
    login_required=True
)
def add_unknown(launch_id, object_id):
    """JRPC method
    Adds a new unknown object to the list.
    :param launch_id: Identifier of the Launch
    :param object_id: Identifier for the unknown object
    :return: Identifier for the unknown object (int)
    """
    return launch_models.Launch.objects.add_unknown(
        launch_id, object_id
    )


@rpc4django.rpcmethod(
    name='leop.launch.removeUnknown',
    signature=['String', 'int'],
    login_required=True
)
def remove_unknown(launch_id, object_id):
    """JRPC method
    Removes an unknown object from the list
    :param launch_id: Identifier of the Launch
    :param object_id: Identifier for the unknown object
    :return: True if the operation was succesful
    """
    return launch_models.Launch.objects.remove_unknown(
        launch_id, object_id
    )


@rpc4django.rpcmethod(
    name='leop.launch.identify',
    signature=['String', 'int', 'String', 'String', 'String'],
    login_required=True
)
def identify(launch_id, object_id, callsign, tle_l1, tle_l2):
    """JRPC method
    Identifies an UFO object and promotes it to an identified one.
    :param launch_id: Identifier of the Launch
    :param object_id: Identifier for the unknown object
    :param callsign: Callsign for the identified object
    :param tle_l1: First line of the TLE associated to the object
    :param tle_l2: Second line of the TLE associated to the object
    :return: Identifier of the promoted object
    """
    object_id, spacecraft_id = launch_models.Launch.objects.identify(
        launch_id, object_id, callsign, tle_l1, tle_l2
    )
    return {
        launch_serial.JRPC_K_OBJECT_ID: object_id,
        launch_serial.JRPC_K_SC_ID: spacecraft_id
    }


@rpc4django.rpcmethod(
    name='leop.launch.forget',
    signature=['String', 'int'],
    login_required=True
)
def forget(launch_id, object_id):
    """JRPC method
    Forgets an identified object and promotes it back to the unknown state.
    :param launch_id: Identifier of the Launch
    :param object_id: Identifier for the unknown object
    :return: True if the operation was succesful
    """
    return launch_models.Launch.objects.forget(launch_id, object_id)


@rpc4django.rpcmethod(
    name='leop.launch.update',
    signature=['String', 'int', 'String', 'String', 'String'],
    login_required=True
)
def update(launch_id, object_id, callsign, tle_l1, tle_l2):
    """JRPC method
    Updates the configuration for a given object.
    :param launch_id: Identifier of the Launch
    :param object_id: Identifier for the unknown object
    :param callsign: Callsign for the identified object
    :param tle_l1: First line of the TLE associated to the object
    :param tle_l2: Second line of the TLE associated to the object
    :return: Identifier of the updated object
    """
    object_id, spacecraft_id = launch_models.Launch.objects.update_identified(
        launch_id, object_id, callsign, tle_l1, tle_l2
    )
    return {
        launch_serial.JRPC_K_OBJECT_ID: object_id,
        launch_serial.JRPC_K_SC_ID: spacecraft_id
    }


@rpc4django.rpcmethod(
    name='leop.getConfiguration',
    signature=['String'],
    login_required=True
)
def get_configuration(launch_id):
    """JRPC method
    Serializes the configuration for the requested LEOP cluster and returns it.
    :param launch_id: The identifier of the LEOP cluster
    :return: JSON-like serialized structure
    """
    launch = launch_models.Launch.objects.get(identifier=launch_id)
    return launch_serial.serialize_launch(launch)


@rpc4django.rpcmethod(
    name='leop.setConfiguration',
    signature=['String', 'Object'],
    login_required=True
)
def set_configuration(launch_id, configuration):
    """JRPC method
    Updates the configuration for a given LAUNCH cluster using the given
    configuration object.
    :param launch_id: Identifier of the launch object
    :param configuration: The new configuration for the launch object
    :return: The identifier of the launch
    """
    launch = launch_models.Launch.objects.get(identifier=launch_id)
    if not configuration:
        raise Exception('Wrong <configuration> object')

    cfg_params = launch_serial.deserialize_launch(configuration)

    launch.update(
        date=cfg_params[0],
        tle_l1=cfg_params[1],
        tle_l2=cfg_params[2]
    )
    return launch.identifier