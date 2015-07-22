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
from preserialize.serialize import serialize


class CompatibilitySerializer(object):
    """
    Class that holds the serializing methods for the Compatibility objects.
    """

    GS_OBJECT_K = 'GroundStation'
    GS_CHANNEL_OBJECT_K = 'GsChannel'

    @staticmethod
    def serialize_gs_ch_compatibility_tuples(gs_ch_list):
        """JSON serializer
        Serializes a list with the tuples of Ground Station and Ground Station
        channels.
        :return: List with the tuples gs, gs_ch in JSON format
        """
        result = []

        for t in gs_ch_list:

            gs_serial = model_to_dict(t[0], fields=['identifier'])
            gs_ch_serial = serialize(
                t[1],
                camelcase=True,
                exclude=['id'],
                related={
                    'band': {
                        'fields': [
                            'IARU_allocation_minimum_frequency',
                            'IARU_allocation_maximum_frequency',
                            'uplink',
                            'downlink'
                        ],
                        'aliases': {
                            'min_freq': 'IARU_allocation_minimum_frequency',
                            'max_freq': 'IARU_allocation_maximum_frequency'
                        }
                    },
                    'modulations': {
                        'fields': ['modulation']
                    },
                    'bandwidths': {
                        'fields': ['bandwidth']
                    },
                    'bitrates': {
                        'fields': ['bitrate']
                    },
                    'polarizations': {
                        'fields': ['polarization']
                    }
                }
            )

            result.append({
                CompatibilitySerializer.GS_OBJECT_K: gs_serial,
                CompatibilitySerializer.GS_CHANNEL_OBJECT_K: gs_ch_serial
            })

        return result
