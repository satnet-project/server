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
from services.accounts import models as account_models
from services.leop.models import launch as leop_models


@rpc4django.rpcmethod(
    name='leop.ufo.add',
    signature=['String', 'int'],
    login_required=True
)
def add(leop_identifier, identifier):
    """JRPC method
    Adds a new UFO object to the cluster.
    :param leop_identifier: Identifier of the LEOP operation that the object
                            belongs to
    :param identifier: Identifier of the object (numerical)
    :return: Identifier of the just created UFO object
    """
    leop = leop_models.Launch.objects.get(identifier=leop_identifier)
    if leop.ufos.filter(identifier=identifier).exists():
        raise Exception(
            'UFO identifier already exists, id = ' + str(identifier)
        )

    leop.ufos = leop.ufos + identifier
    leop.save(update_fields=['ufos'])
    return identifier


@rpc4django.rpcmethod(
    name='leop.ufo.remove',
    signature=['String', 'int'],
    login_required=True
)
def remove(leop_identifier, identifier):
    """JRPC method
    Removes an UFO object from the cluster
    :param leop_identifier: Identifier of the LEOP operation that the object
                            belongs to
    :param identifier: Identifier of the object (numerical)
    :return: Identifier of the just created UFO object
    """
    leop = leop_models.Launch.objects.get(identifier=leop_identifier)
    leop.cluster.all().get(identifier=identifier).delete()
    return identifier


@rpc4django.rpcmethod(
    name='leop.ufo.identify',
    signature=['String', 'int', 'String', 'String', 'String'],
    login_required=True
)
def identify(leop_identifier, identifier, callsign, tle_l1, tle_l2, **kwargs):
    """JRPC method
    Promotes a given UFO object into the <identified> state by associating a
    TLE and callsign to it. Basically, it permits detaching this object from the
    cluster and generates the associated GroundTrack for its simulation.
    :param leop_identifier: Identifier of the LEOP operation that the object
                            belongs to
    :param identifier: Identifier of the object (numerical)
    :param callsign: Alias for the new <identified> object
    :param tle_l1: First line of the TLE for this object
    :param tle_l2: Second line of the TLE for this object
    :return: Identifier of the just created UFO object
    """
    leop = leop_models.Launch.objects.get(identifier=leop_identifier)
    user = kwargs.get('request', None).user
    profile = account_models.UserProfile.objects.get(username=user)
    leop.identify_ufo(profile, identifier, callsign, tle_l1, tle_l2)
    return identifier


@rpc4django.rpcmethod(
    name='leop.ufo.update',
    signature=['String', 'int', 'String', 'String', 'String'],
    login_required=True
)
def update(leop_identifier, identifier, callsign, tle_l1, tle_l2):
    """JRPC method
    Updates a given UFO object with the value that change in this new
    configuration.
    :param leop_identifier: Identifier of the LEOP operation that the object
                            belongs to
    :param identifier: Identifier of the object (numerical)
    :param callsign: Alias for the new <identified> object
    :param tle_l1: First line of the TLE for this object
    :param tle_l2: Second line of the TLE for this object
    :return: Identifier of the just created UFO object
    """
    leop = leop_models.Launch.objects.get(identifier=leop_identifier)
    leop.update_ufo(identifier, callsign, tle_l1, tle_l2)
    return identifier


@rpc4django.rpcmethod(
    name='leop.ufo.forget',
    signature=['String', 'int'],
    login_required=True
)
def forget(leop_identifier, identifier):
    """JRPC method
    Anonymizes a given UFO object that had previously been identified.
    :param leop_identifier: Identifier of the LEOP operation that the object
                            belongs to
    :param identifier: Identifier of the object (numerical)
    :return: Identifier of the just created UFO object
    """
    leop = leop_models.Launch.objects.get(identifier=leop_identifier)
    ufo = leop.cluster.all().get(identifier=identifier)
    x = ufo.spacecraft.identifier
    ufo.forget()
    return identifier