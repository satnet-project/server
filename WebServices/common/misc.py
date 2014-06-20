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

from datetime import datetime, time
# noinspection PyDeprecation
from django.utils import simplejson
from pytz import utc as pytz_utc
import sys
import urllib2

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


___G_API_ALTITUDE_URL__ = 'http://maps.googleapis.com/maps/api/elevation/'
___G_API_ALTITUDE_OUTPUT__ = [
    'json',
    'xml'
]


def get_altitude(latitude, longitude):
    """
    This method returns the altitude for a point specified as a pair of
    coordinates (latitude, longitude).
    The full format for the Google API to retrieve the altitude for a given
    point given as a pair (latitude, longitude) is the following:
        proto://maps.googleapis.com/maps/api/elevation/outputFormat?parameters
    ... where:
    *) proto = ['https', 'http']
    *) outputFormat = ['json', 'xml']
    *) parameters = {locations=latitude,longitude}
    *) RESULT = (JSON object)
        {
            "results" : [ {
                "elevation" : 1608.637939453125,
                "location" : {
                    "lat" : 39.73915360,
                    "lng" : -104.98470340
                },
                "resolution" : 4.771975994110107
            }],
            "status" : "OK"
        }
    :param latitude: The latitude for the given point.
    :param longitude: The longitude for the given point.
    :return: A tuple (h, r) with the altitude (h, in meters) and the
    resolution (r, in meters). The resolution (r) represents the maximum
    distance (in meters) between data points from which the elevation was
    interpolated.
    """
    # noinspection PyDeprecation
    r = simplejson.loads(
        urllib2.urlopen(
            ___G_API_ALTITUDE_URL__
            + ___G_API_ALTITUDE_OUTPUT__[0]
            + '?locations='
            + str(latitude) + ',' + str(longitude)
        ).read()
    )
    return r['results'][0]['elevation'], r['results'][0]['resolution']


def print_list(l, list_name='List'):
    """
    Function that prints the elements of a given list, one per line.
    :param l: The list to be printed out.
    """
    print '>>>>>>> PRINTING ' + list_name + ', len = ' + str(len(l))
    for l_i in l:
        print l_i


def list_2_string(l, list_name='List'):
    """
    Function that prints the elements of the given list, one per line,
    in a string.
    :param l: The list to be print out.
    :param list_name: The name for the list.
    :return: String with the contents of the list with no \n trailing
                character.
    """
    if not l:
        return '(empty list)'

    o_string = '[\n'
    for l_i in l:
        o_string += '\t' + str(l_i) + '\n'
    o_string += ']'

    return o_string


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


def get_today_utc(no_microseconds=True):
    """
    This method returns today's date localized with the microseconds set to
    zero.
    :param no_microseconds=True: sets whether microseconds should be cleared.
    :return: the just created datetime object with today's date.
    """
    if no_microseconds:
        return pytz_utc.localize(datetime.today()).replace(microsecond=0)
    else:
        return pytz_utc.localize(datetime.today())


def localize_date_utc(date):
    """
    Localizes in the UTC timezone the given date object.
    :param date: The date object to be localized.
    :return: A localized datetime object in the UTC timezone.
    """
    return pytz_utc.localize(datetime.combine(date, time(
        hour=0, minute=0, second=0))
    )


def localize_time_utc(non_utc_time):
    """
    Localizes in the UTC timezone the given time object.
    :param non_utc_time: The time object to be localized.
    :return: A localized time object in the UTC timezone.
    """
    return pytz_utc.localize(non_utc_time)

__TIMESTAMP_0 = localize_date_utc(datetime(year=1970, month=1, day=1))


def get_utc_timestamp(utc_datetime=None):
    """
    Returns a timestamp with the number of miliseconds ellapsed since January
    1st of 1970 for the given datetime object, UTC localized.
    :param utc_datetime: The datetime whose timestamp is to be calculated.
    :return: The number of seconds since 1.1.1970, UTC localized.
    """
    diff = utc_datetime - __TIMESTAMP_0
    return diff.total_seconds() * 10**3