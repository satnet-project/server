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


@rpc4django.rpcmethod(
    name='leop.ufo.add',
    signature=['int'],
    login_required=True
)
def add(identifier):
    """
    Adds a new UFO object to the cluster.
    :param identifier: Identifier of the object (numerical)
    :return: True if the operation was completed correctly
    """
    pass


@rpc4django.rpcmethod(
    name='leop.ufo.remove',
    signature=['int'],
    login_required=True
)
def remove(identifier):
    """
    Removes an UFO object from the cluster
    :param identifier: Identifier of the object (numerical)
    :return: True if the operation was completed correctly
    """
    pass


@rpc4django.rpcmethod(
    name='leop.ufo.identify',
    signature=['int', 'String', 'String', 'String'],
    login_required=True
)
def identify(identifier, alias, tle_l1, tle_l2):
    pass


@rpc4django.rpcmethod(
    name='leop.ufo.update',
    signature=['int', 'String', 'String', 'String'],
    login_required=True
)
def update(identifier, alias, tle_l1, tle_l2):
    pass


@rpc4django.rpcmethod(
    name='leop.ufo.forget',
    signature=['int'],
    login_required=True
)
def forget(identifier):
    pass