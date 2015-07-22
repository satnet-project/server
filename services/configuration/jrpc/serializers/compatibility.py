"""
   Copyright 2015 Ricardo Tubio-Pardavila

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

from django.forms.models import model_to_dict


class CompatibilitySerializer(object):
    """
    Class that holds the serializing methods for the Compatibility objects.
    """

    GS_OBJECT_K = 'groundstation'
    GS_CHANNEL_OBJECT_K = 'gs_channel'

    @staticmethod
    def serialize_gs_ch_compatibility_tuples(gs_ch_list):
        """JSON serializer
        Serializes a list with the tuples of Ground Station and Ground Station
        channels.
        :return: List with the tuples gs, gs_ch in JSON format
        """
        result = []

        for t in gs_ch_list:

            gs_serial = model_to_dict(t[0])
            gs_ch_serial = model_to_dict(t[1])

            result.append({
                'groundstation': gs_serial,
                'gs_channel': gs_ch_serial
            })

        return result
