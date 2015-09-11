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

from rpc4django import rpcmethod
import socket
from services.common import gis
from website import settings as satnet_settings


@rpcmethod(
    name='network.alive',
    signature=[],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def keep_alive():
    """JRPC method
    Simple method used to keep alive the server connection.
    :return: True
    """
    return True


@rpcmethod(
    name='network.geoip',
    signature=['String'],
    login_required=False
)
def hostname_geoip(hostname):
    """JRPC method
    Retrieves the location of the given hostname using the GEO IP services.
    :param hostname: The name of the host
    :return: JSON object, { latitude: $lat, longitude: $lng }
    """

    host_ip = socket.gethostbyname(hostname)
    lat, lng = gis.get_remote_user_location(ip=host_ip)

    print('>>> host = ' + str(hostname) + ', ip = ' + str(host_ip) +
          ', @(' + str(lat) + ', ' + str(lng) + ')')

    return {'latitude': lat, 'longitude': lng}
