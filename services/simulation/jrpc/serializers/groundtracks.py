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

import datetime
from services.common import misc


class SimulationSerializer(object):
    """JSON-RPC serializer.
    Serializer for the Simulation-related objects from the database.
    """

    _DECIMATION_RATE = 1
    _PERIOD = datetime.timedelta(hours=8)

    TIMESTAMP_K = 'timestamp'
    LATITUDE_K = 'latitude'
    LONGITUDE_K = 'longitude'

    @staticmethod
    def serialize_groundtrack(groundtrack):
        """JSON-RPC method.
        JSON remotelly invokable method that returns the estimated groundtrack
        for a given spacecraft.
        :param groundtrack: The estimated groundtrack.
        :return: Array containing objects of the type
                    { 'timestamp', 'latitude', 'longitude' }.
        """
        result = []
        index = 0
        ts_l, la_l, lo_l = groundtrack.read()
        gt_length = len(ts_l)

        start_date = misc.get_now_utc()
        end_date = start_date + SimulationSerializer._PERIOD
        start_ts = start_date.timestamp()
        end_ts = end_date.timestamp()

        while index < gt_length:

            ts_i = ts_l[index]

            if ts_i > end_ts:
                break

            if ts_i > start_ts:
                result.append({
                    SimulationSerializer.TIMESTAMP_K: ts_i,
                    SimulationSerializer.LATITUDE_K: la_l[index],
                    SimulationSerializer.LONGITUDE_K: lo_l[index]
                })

            index += SimulationSerializer._DECIMATION_RATE

        return result
