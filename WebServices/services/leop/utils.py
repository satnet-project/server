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


class ConstantGenerators(object):
    """Utils class
    Class with multiple static methods utilized for generating constant values
    such as identifiers.
    """
    @staticmethod
    def generate_sc_identifier(identifier, callsign):
        """Generates SC ID
        Generates the identifier for the simulation-only-purposes spacecraft
        that represents this UFO object.
        :param identifier: Identifier of the UFO (sequential number)
        :param callsign: Callsign for the UFO
        :return: String with the complete TLE source
        """
        sc_id = 'ufo:' + str(identifier) + ':cs:' + str(callsign)
        return sc_id[0:(segment_models.Spacecraft.MAX_SC_ID_LEN - 1)]

    @staticmethod
    def generate_ufo_tle_source(identifier):
        """UFO TLE Source Generator
        Generates the identificator for the source of the UFO TLE files.
        :param identifier: Identifier of the UFO (sequential number)
        :return: String with the complete TLE source
        """
        return 'tle://' + socket.getfqdn() + '/ufo/' + str(identifier)

    @staticmethod
    def generate_ufo_tle_id(identifier, callsign):
        """UFO TLE ID generator
        Generates a complex UFO identifier that is to be used as the initial
        identifier of the associated TLE in the database.
        :param identifier: Identifier of the UFO (sequential number)
        :param callsign: Callsign for the UFO
        :return: String with the complete TLE source
        """
        tle_id = 'ufo:' + str(identifier) + ':cs:' + str(callsign)
        return tle_id[0:(tle_models.TwoLineElement.MAX_TLE_ID_LEN - 1)]

    @staticmethod
    def create_ufo_tle(identifier, callsign, tle_l1, tle_l2):
        """Object method
        Creates a TLE for this UFO object.
        :param identifier: Identifier of the UFO object
        :param callsign: Callsign for the UFO
        :param tle_l1: First line of the UFO's TLE
        :param tle_l2: Second line of the UFO's TLE
        :return: Reference to the just-created object
        """
        tle_source = ConstantGenerators.generate_ufo_tle_source(identifier)
        tle_id = ConstantGenerators.generate_ufo_tle_id(identifier, callsign)
        return tle_models.TwoLineElement.objects.create(
            source=tle_source, l0=tle_id, l1=tle_l1, l2=tle_l2
        )