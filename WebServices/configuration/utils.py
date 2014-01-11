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

import urllib2
import logging
logger = logging.getLogger(__name__)

from django.utils import simplejson

__SLO_LAT__ = 35.347099
__SLO_LON__ = -120.455299


def get_remote_user_location(ip=None,
                             geoplugin_ip=
                             'http://www.geoplugin.net/json.gp?ip='):
    """
    This method returns the current geolocation of a given IP address by using
    the WebService provided by GeoPlugin. In case no ip address is given, it
    returns None.
    """

    if not ip:
        return None
    if ip == "127.0.0.1":
        return __SLO_LAT__, __SLO_LON__

    json_r = urllib2.urlopen(geoplugin_ip + ip).read()
    r = simplejson.loads(json_r)
    latitude = r['geoplugin_latitude']
    longitude = r['geoplugin_longitude']

    return latitude, longitude
