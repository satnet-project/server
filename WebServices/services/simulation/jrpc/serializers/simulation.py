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


class SimulationSerializer(object):
    """JSON-RPC serializer.
    Serializer for the Simulation-related objects from the database.
    """

    TIMESTAMP_K = 'timestamp'
    LATITUDE_K = 'latitude'
    LONGITUDE_K = 'longitude'

    def serialize_groundtrack(self, groundtrack):
        """JSON-RPC method.
        JSON remotelly invokable method that returns the estimated groundtrack
        for a given spacecraft.
        :param groundtrack: The estimated groundtrack.
        :return: Array containing objects of the type
                    { 'timestamp', 'latitude', 'longitude' }.
        """
        result = []
        index = 0

        for ts in groundtrack.timestamp:

            result.append({
                SimulationSerializer.TIMESTAMP_K: ts,
                SimulationSerializer.LATITUDE_K: groundtrack.latitude[index],
                SimulationSerializer.LONGITUDE_K: groundtrack.longitude[index]
            })

            index += 1

        return result