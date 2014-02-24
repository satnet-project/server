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
import sys
import logging
logger = logging.getLogger(__name__)

# noinspection PyDeprecation
from django.utils import simplejson

__SLO_LAT__ = 35.347099
__SLO_LON__ = -120.455299
__GEOIP_URL__ = 'http://www.geoplugin.net/json.gp?ip='


def get_remote_user_location(ip=None, geoplugin_ip=__GEOIP_URL__):
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
    # noinspection PyDeprecation
    r = simplejson.loads(json_r)
    latitude = r['geoplugin_latitude']
    longitude = r['geoplugin_longitude']

    return latitude, longitude


def print_dictionary(obj, nested_level=0, output=sys.stdout, spacing='   '):
    """
    Function that recursively prints a dict and all its nested dictionaries.
    :param obj: the dictionary to be printed.
    :param nested_level: used to increase the spacing for items in between
    nested dictionaries.
    :param output: the output where the function prints the data from the
    dictionaries.
    :param spacing: the string used as a base for spacing items in between
    dictionaries.
    """
    if type(obj) == dict:
        print >> output, '%s{' % (nested_level * spacing)
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print >> output, '%s%s:' % ((nested_level + 1) * spacing, k)
                print_dictionary(v, nested_level + 1, output)
            else:
                print >> output, '%s%s: %s' % ((nested_level + 1) * spacing,
                                               k, v)
        print >> output, '%s}' % (nested_level * spacing)
    elif type(obj) == list:
        print >> output, '%s[' % (nested_level * spacing)
        for v in obj:
            if hasattr(v, '__iter__'):
                print_dictionary(v, nested_level + 1, output)
            else:
                print >> output, '%s%s' % ((nested_level + 1) * spacing, v)
        print >> output, '%s]' % (nested_level * spacing)
    else:
        print >> output, '%s%s' % (nested_level * spacing, obj)
