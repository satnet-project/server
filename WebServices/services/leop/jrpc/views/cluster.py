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
from services.leop.models import leop as leop_models
from services.leop.jrpc.serializers import cluster as cluster_serial


@rpc4django.rpcmethod(
    name='leop.gs.list',
    signature=['String'],
    login_required=True
)
def list_groundstations(leop_id, **kwargs):
    """JRPC method (LEOP service).
    Returns the list of groundstations available for creating this LEOP
    system. In case a Ground Station is already in use for this system, it will
    not be listed.
    :param leop_id: Identifier of the LEOP cluster.
    :param kwargs: Dictionary with additional variables like the HTTP request
                    itself (defined by RPC4Django).
    :return: List of the identifiers of the available groundstations.
    """

    # user must be obtained from the request, since this has already been
    # validated by the authentication backend
    http_request = kwargs.get('request', None)
    if not http_request or not http_request.user.is_staff:
        raise django_ex.PermissionDenied()

    leop_cluster = leop_models.LEOP.objects.get(identifier=leop_id)

    # List construction: ground stations in use and available for LEOP
    u_gs = leop_cluster.groundstations.all()
    all_gs = segment_models.GroundStation.objects.all()
    a_gs = [item for item in all_gs if item not in u_gs]

    # Serialization to a JSON-RPC-like object
    return cluster_serial.serialize_gs_lists(a_gs, u_gs)


@rpc4django.rpcmethod(
    name='leop.gs.add',
    signature=['String', 'Object'],
    login_required=True
)
def add_groundstations(leop_id, groundstations, **kwargs):
    """JRPC method (LEOP service).
    Adds the array of GroundStations to the LEOP cluster. If any of the given
    GroundStation identifiers does not exist, the operation is cancelled and
    an 'ObjectDoesNotExist' exception is raised.
    :param leop_id: Identifier of the LEOP cluster.
    :param groundstations: List with the GroundStations to be added.
    :return: Identifier of the just-updated LEOP cluster.
    """

    # user must be obtained from the request, since this has already been
    # validated by the authentication backend
    http_request = kwargs.get('request', None)
    if not http_request or not http_request.user.is_staff:
        raise django_ex.PermissionDenied()

    # find the cluster object and add the ground stations to it
    leop_cluster = leop_models.LEOP.objects.get(identifier=leop_id)

    # If no groundstations are provided but the leop cluster exists and the user
    # has the appropriate permissions, this case is considered to be a correct
    # execution.
    if not groundstations:
        return cluster_serial.serialize_leop_id(leop_id)

    for g_id in groundstations:

        g = segment_models.GroundStation.objects.get(identifier=g_id)
        leop_cluster.groundstations.add(g)

    leop_cluster.save()

    # Serialization to a JSON-RPC-like object
    return cluster_serial.serialize_leop_id(leop_id)


@rpc4django.rpcmethod(
    name='leop.gs.remove',
    signature=['String', 'Object'],
    login_required=True
)
def remove_groundstations(leop_id, groundstations, **kwargs):
    """JRPC method (LEOP service).
    Removes the array of GroundStations from the LEOP cluster. If any of the
    given GroundStation identifiers does not exist, the operation is
    cancelled and an 'ObjectDoesNotExist' exception is raised.
    :param leop_id: Identifier of the LEOP cluster.
    :param groundstations: List with the GroundStations to be added.
    :return: Identifier of the just-updated LEOP cluster.
    """

    # user must be obtained from the request, since this has already been
    # validated by the authentication backend
    http_request = kwargs.get('request', None)
    if not http_request or not http_request.user.is_staff:
        raise django_ex.PermissionDenied()

    # find the cluster object and add the ground stations to it
    leop_cluster = leop_models.LEOP.objects.get(identifier=leop_id)

    # If no groundstations are provided but the leop cluster exists and the user
    # has the appropriate permissions, this case is considered to be a correct
    # execution.
    if not groundstations:
        return cluster_serial.serialize_leop_id(leop_id)

    for g_id in groundstations:

        g = leop_cluster.groundstations.get(identifier=g_id)
        leop_cluster.groundstations.remove(g)

    leop_cluster.save()

    # Serialization to a JSON-RPC-like object
    return cluster_serial.serialize_leop_id(leop_id)