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

import base64
import logging
from services.common import misc

logger = logging.getLogger('common')


AX25_FLAG = 0x7E
AX25_ADDRESS_MIN_LEN = 14
AX25_ADDRESS_MAX_LEN = 28


class AX25Packet(object):
    """
    Simple AX25 packet decoder.
    """

    flag = 0x7E
    destination = ''
    source = ''

    raw_packet = None

    def __unicode__(self):
        """Unicode string
        Representation of this object as an Unicode string.
        :return: Unicode string
        """
        return misc.dict_2_string({
            'raw_packet': self.raw_packet,
            'flag': self.flag,
            'destination': self.destination,
            'source': self.source
        })


def decode_base64(string):
    """Factory-like decoder
    Simple method for decoding the basic fields from the AX.25 frame that
    comes in a BASE64 string.
    :param string: BASE 64 string with the AX.25 frame
    :return: AX.25 packet object
    """
    p = AX25Packet()
    p.raw_packet = base64.b64decode(string)

    return p