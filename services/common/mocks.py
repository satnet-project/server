"""
   Copyright 2016 Ricardo Tubio-Pardavila

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


import datetime
import ephem
from services.common import misc as sn_misc


class mock__OrbitalSimulator(object):

    @staticmethod
    def dbtle_2_ephem_str(spacecraft_tle):
        return sn_misc.unicode_2_string(spacecraft_tle.identifier),\
            sn_misc.unicode_2_string(spacecraft_tle.first_line),\
            sn_misc.unicode_2_string(spacecraft_tle.second_line)

    @staticmethod
    def create_spacecraft(l0, l1, l2):
        if isinstance(l0, bytes):
            l0 = str(l0, 'ascii')
        if isinstance(l1, bytes):
            l1 = str(l1, 'ascii')
        if isinstance(l2, bytes):
            l2 = str(l2, 'ascii')
        return ephem.readtle(l0, l1, l2)

    @staticmethod
    def get_simulation_window():
        return (
            sn_misc.get_now_utc(),
            sn_misc.get_next_midnight() + datetime.timedelta(days=2)
        )

    # noinspection PyMethodMayBeStatic
    def calculate_pass_slot(
        self, start, end, minimum_slot_duration=datetime.timedelta(minutes=1)
    ):

        half = (end - start).seconds / 2
        return [
            (
                start + datetime.timedelta(seconds=half),
                start + datetime.timedelta(seconds=(half + 60))
            )
        ]

    # noinspection PyMethodMayBeStatic
    def calculate_groundtrack(
        self, spacecraft_tle, interval=None,
        timestep=datetime.timedelta(seconds=20)
    ):

        d_0 = datetime.datetime.utcnow()

        return [{
            'timestamp': d_0,
            'latitude': 10.0,
            'longitude': 10
        }]
