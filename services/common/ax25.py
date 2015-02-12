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

    FLAG = b'7E'
    FLAG_LEN = len(FLAG)
    DEST_ADDR_LEN = 14  # 2 chars per byte
    SRC_ADDR_LEN = 14  # 2 chars per byte
    PID_LEN = 2  # 2 chars per byte
    FCS_LEN = 4  # 2 chars per byte

    START_FLAG_POS = 0
    # END_FLAG_POS is calculated dynamically depending on the actual size
    # of the frame
    DEST_ADDR_POS = START_FLAG_POS + FLAG_LEN
    SRC_ADDR_POS = DEST_ADDR_POS + DEST_ADDR_LEN
    PID_POS = SRC_ADDR_POS + SRC_ADDR_LEN
    FCS_POS = PID_POS + PID_LEN

    ADDRESS_MIN_LEN = DEST_ADDR_LEN + SRC_ADDR_LEN
    ADDRESS_MAX_LEN = 2 * ADDRESS_MIN_LEN  # in case there is a repeater
    MIN_LEN = FLAG_LEN + ADDRESS_MIN_LEN

    raw_packet = None

    start_flag = None

    destination = None
    source = None

    pid = None
    fcs = None

    end_flag = None

    @staticmethod
    def _check_hexstring(string, read_pid, read_fcs):
        """
        Checks the validity of the given hex string.
        :param string: String to be checked
        :return: (String, int) Raw packet in hex string (2 chars/B) and the len
                                of that hex string
        """

        if not string:
            raise Exception('<string> is empty')

        raw_packet = base64.b64decode(string)

        hexstr_len = len(raw_packet)
        if (hexstr_len % 2) != 0:
            raise Exception(
                '<string> len is supposed to be even, truncated bytes?'
            )
        min_len = AX25Packet._calculate_min_len(read_pid, read_fcs)
        if hexstr_len < min_len:
            raise Exception(
                '<string> too short: ' + str(hexstr_len) + ' < ' + str(min_len)
            )

        return raw_packet, hexstr_len

    @staticmethod
    def _calculate_min_len(read_pid, read_fcs):
        """
        Calculates the minimum possible length for the expected packet.
        :param read_pid: Flag that indicates whether the PID field is read
        :param read_fcs: Flag that indicates whether the FCS field is read
        :return: Integer with the minimum length for a hex string (2 chars/B)
        """
        min_len = AX25Packet.MIN_LEN
        if read_pid:
            min_len += AX25Packet.PID_LEN
        if read_fcs:
            min_len += AX25Packet.FCS_LEN
        return min_len

    @staticmethod
    def decode_base64(string, read_pid=False, read_fcs=False):
        """Factory-like decoder
        Simple method for decoding the basic fields from the AX.25 frame that
        comes in a BASE64 string.
        :param string: BASE 64 string with the AX.25 frame
        :return: AX.25 packet object
        """
        p = AX25Packet()
        p.raw_packet, hexstr_len = AX25Packet._check_hexstring(
            string, read_pid, read_fcs
        )

        flag = p.raw_packet[AX25Packet.START_FLAG_POS:AX25Packet.FLAG_LEN]
        if flag != AX25Packet.FLAG:
            raise Exception('Packet does not start with mandatory FLAG')
        p.start_flag = flag

        flag = p.raw_packet[(hexstr_len - AX25Packet.FLAG_LEN):hexstr_len]
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

        if read_pid:
            p.pid = p.raw_packet[
                AX25Packet.PID_POS:
                AX25Packet.PID_POS + AX25Packet.PID_LEN
            ]
        if read_fcs:
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
        p_dict = {}

        if self.raw_packet:
            p_dict['raw_packet'] = self.raw_packet
        if self.start_flag:
            p_dict['start_flag'] = self.start_flag
        if self.destination:
            p_dict['destination'] = self.destination
        if self.source:
            p_dict['source'] = self.source
        if self.pid:
            p_dict['pid'] = self.pid
        if self.fcs:
            p_dict['fcs'] = self.fcs
        if self.end_flag:
            p_dict['end_flag'] = self.end_flag

        return p_dict

    def __unicode__(self):
        """Unicode string
        Representation of this object as an Unicode string.
        :return: Unicode string
        """
        return misc.dict_2_string(self.as_dictionary())