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


class AX25Packet(object):
    """
    Simple AX25 packet decoder.
    """

    FLAG = '7E'
    FLAG_LEN = len(FLAG)
    DEST_ADDR_LEN = 14  # 2 chars per byte
    SRC_ADDR_LEN = 14  # 2 chars per byte
    PID_LEN = 2  # 2 chars per byte
    FCS_LEN = 4  # 2 chars per byte

    START_FLAG_POS = 0
    DEST_ADDR_POS = START_FLAG_POS + FLAG_LEN
    SRC_ADDR_POS = DEST_ADDR_POS + DEST_ADDR_LEN
    PID_POS = SRC_ADDR_POS + SRC_ADDR_LEN
    FCS_POS = PID_POS + PID_LEN

    ADDRESS_MIN_LEN = DEST_ADDR_LEN + SRC_ADDR_LEN
    ADDRESS_MAX_LEN = 2 * ADDRESS_MIN_LEN  # in case there is a repeater

    MIN_LEN = FLAG_LEN + ADDRESS_MIN_LEN + PID_LEN + FCS_LEN  # 2 B/char

    raw_packet = None

    start_flag = ''

    destination = ''
    source = ''

    pid = ''
    fcs = ''

    end_flag = ''

    @staticmethod
    def decode_base64(string):
        """Factory-like decoder
        Simple method for decoding the basic fields from the AX.25 frame that
        comes in a BASE64 string.
        :param string: BASE 64 string with the AX.25 frame
        :return: AX.25 packet object
        """
        if not string:
            raise Exception('<string> is empty')

        raw_packet = base64.b64decode(string)

        str_len = len(raw_packet)
        if (str_len % 2) != 0:
            raise Exception(
                '<string> len is supposed to be even, truncated bytes?'
            )
        if str_len < AX25Packet.MIN_LEN:
            raise Exception(
                '<string> is too short: ' + str(str_len) +
                ', expected = ' + str(AX25Packet.MIN_LEN)
            )

        p = AX25Packet()
        p.raw_packet = raw_packet

        flag = p.raw_packet[AX25Packet.START_FLAG_POS:AX25Packet.FLAG_LEN]
        if flag != AX25Packet.FLAG:
            raise Exception('Packet does not start with mandatory FLAG')
        p.start_flag = flag

        flag = p.raw_packet[(str_len - AX25Packet.FLAG_LEN):str_len]
        if flag != AX25Packet.FLAG:
            raise Exception('Packet does not end with mandatory FLAG')
        p.end_flag = AX25Packet.FLAG

        p.destination = p.raw_packet[
            AX25Packet.DEST_ADDR_POS:
            AX25Packet.DEST_ADDR_POS + AX25Packet.DEST_ADDR_LEN
        ]
        p.source = p.raw_packet[
            AX25Packet.SRC_ADDR_POS:
            AX25Packet.SRC_ADDR_POS + AX25Packet.SRC_ADDR_LEN
        ]
        p.pid = p.raw_packet[
            AX25Packet.PID_POS:
            AX25Packet.PID_POS + AX25Packet.PID_LEN
        ]
        p.fcs = p.raw_packet[
            AX25Packet.FCS_POS:
            AX25Packet.FCS_POS + AX25Packet.FCS_LEN
        ]

        return p

    def as_dictionary(self):
        """
        Returns all the fields of this packet within a dictionary.
        :return: JSON-like dictionary with the packet contents
        """
        return {
            'raw_packet': self.raw_packet,
            'start_flag': self.start_flag,
            'destination': self.destination,
            'source': self.source,
            'PID': self.pid,
            'FCS': self.fcs,
            'end_flag': self.end_flag
        }

    def __unicode__(self):
        """Unicode string
        Representation of this object as an Unicode string.
        :return: Unicode string
        """
        return misc.dict_2_string(self.as_dictionary())