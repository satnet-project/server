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

from services.configuration.jrpc.serializers import serialization as \
    segment_serializers


class TleSerializer(object):
    """
    Class that holds the serializers methods for the TLE objects.
    """

    # JSON key for the line 1 field.
    TLE_LINE_1_K = 'tle_line_1'
    # JSON key for the line 2 field.
    TLE_LINE_2_K = 'tle_line_2'

    # Length of Line 1.
    LEN_TLE_LINE_1 = 69
    # Length of Line 2.
    LEN_TLE_LINE_2 = 69

    @staticmethod
    def serialize(spacecraft):
        """
        Method that serializes the information from a Spacecraft object
        including the information of the related TLE object.
        :param spacecraft: Spacecraft whose TLE has to be serialized.
        :return: Object { spacecraft_id, tle_id, tle_line_1, tle_line_2 }
        """
        if spacecraft.tle is None:
            raise Exception(
                'No TLE found for Spacecraft, id = <'
                + str(spacecraft.identifier) + '>'
            )
        else:
            return {
                segment_serializers.SC_ID_K: spacecraft.identifier,
                segment_serializers.SC_TLE_ID_K: spacecraft.tle.identifier,
                TleSerializer.TLE_LINE_1_K: spacecraft.tle.first_line,
                TleSerializer.TLE_LINE_2_K: spacecraft.tle.second_line
            }