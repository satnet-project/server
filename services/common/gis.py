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

import logging

from services.common import misc

logger = logging.getLogger('common')

__SLO_LAT__ = 35.347099
__SLO_LON__ = -120.455299
__GEOIP_URL__ = 'http://www.geoplugin.net/json.gp?ip='


def get_remote_user_location(ip=None, geoplugin_ip=__GEOIP_URL__):
    """
    This method returns the current geolocation of a given IP address by using
    the WebService provided by GeoPlugin. In case no ip address is given, it
    returns None.
    :param ip: IP address for the remote user
    :param geoplugin_ip: URL of the WebService to resolve the IP address
    """
    if not ip:
        return __SLO_LAT__, __SLO_LON__
    if ip == "127.0.0.1":
        return __SLO_LAT__, __SLO_LON__

    r = misc.load_json_url(geoplugin_ip + ip)

    latitude = r['geoplugin_latitude']
    longitude = r['geoplugin_longitude']

    return latitude, longitude


__G_API_GEOCODE_URL__ = 'http://maps.googleapis.com/maps/api/geocode/'
__G_API_GEOCODE_OUTPUT__ = ['json', 'xml']
__G_API_ADDRESS_COUNTRY_AREA__ = 'country'
__G_API_ADDRESS_REGION_AREA__ = 'administrative_area_level_1'
__G_API_RESULTS_ARRAY__ = 'results'
__G_API_ADDRESS_ITEM__ = 0
__G_API_ADDRESS_ARRAY__ = 'address_components'
__G_API_TYPES_ARRAY__ = 'types'
__G_API_LONG_NAME__ = 'long_name'
__G_API_SHORT_NAME__ = 'short_name'

COUNTRY_LONG_NAME = 'country-l'
COUNTRY_SHORT_NAME = 'country-s'
REGION_SHORT_NAME = 'region-s'
REGION_LONG_NAME = 'region-l'


def get_region(latitude, longitude):
    """
    This method returns the formatted name of the country to which this
    position belongs to.
    :param latitude: The latitude for the given point.
    :param longitude: The longitude for the given point.
    :return: {country-long, country-short, region-long, region-short}.
    """
    url = __G_API_GEOCODE_URL__\
        + __G_API_GEOCODE_OUTPUT__[0]\
        + '?latlng='\
        + str(latitude) + ',' + str(longitude)\
        + '&sensor=true'

    r = misc.load_json_url(url)

    country_l, country_s, region_l, region_s = '', '', '', ''
    country_found = False
    region_found = False

    try:

        address_list = r[
            __G_API_RESULTS_ARRAY__
        ][
            __G_API_ADDRESS_ITEM__
        ][
            __G_API_ADDRESS_ARRAY__
        ]

        for a in address_list:
            for t in a[__G_API_TYPES_ARRAY__]:
                if t == __G_API_ADDRESS_COUNTRY_AREA__:
                    country_l = a[__G_API_LONG_NAME__]
                    country_s = a[__G_API_SHORT_NAME__]
                    country_found = True
                if t == __G_API_ADDRESS_REGION_AREA__:
                    region_l = a[__G_API_LONG_NAME__]
                    region_s = a[__G_API_SHORT_NAME__]
                    region_found = True

    except IndexError as ex:
        logger.exception(
            'IndexError thrown, region information not consistent for' +
            ': (lat = ' + str(latitude) + ', lng = ' + str(longitude) + ')' +
            ', ex = ' + str(ex),
            ex
        )

    if not country_found and not region_found:
        raise Exception('Could not find country and region information.')

    return {
        COUNTRY_LONG_NAME: country_l,
        COUNTRY_SHORT_NAME: country_s,
        REGION_LONG_NAME: region_l,
        REGION_SHORT_NAME: region_s
    }


___G_API_ALTITUDE_URL__ = 'http://maps.googleapis.com/maps/api/elevation/'
___G_API_ALTITUDE_OUTPUT__ = ['json', 'xml']


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
    url = ___G_API_ALTITUDE_URL__ + ___G_API_ALTITUDE_OUTPUT__[0] + \
        '?locations=' + str(latitude) + ',' + str(longitude)
    r = misc.load_json_url(url)

    return r['results'][0]['elevation'], r['results'][0]['resolution']


def get_latitude_direction(latitude_degrees):
    """
    Returns the direction for the given latitude degrees.
    :param latitude_degrees: The degrees (not minutes) as an integer.
    :return: String containing the possible latitude directions (N, S).
    """
    if latitude_degrees is None:
        raise ValueError('No value provided for <latitude_degrees>')

    if latitude_degrees < 0:
        return "S"
    elif latitude_degrees > 0:
        return "N"
    else:
        return ""


def get_longitude_direction(longitude_degrees):
    """
    Returns the direction for the given longitude degrees.
    :param longitude_degrees: The degrees (not minutes) as an integer.
    :return: String containing the possible latitude directions (W, E).
    """
    if longitude_degrees is None:
        raise ValueError('No value provided for <longitude_degrees>')

    if longitude_degrees < 0:
        return "W"
    elif longitude_degrees > 0:
        return "E"
    else:
        return ""


def latlng_2_degrees(latlng, add_direction=False):
    """
    Converts a latlng coordinate position from decimal degrees into DMS format.
    :param latlng: Coordinate in decimal format
    :param add_direction: Marks whether direction should be added or not
    :return: Tuple with the DMS-formatted (lat, lng)
    """
    return decimal_2_degrees(
        latlng[0], latitude=True, add_direction=add_direction
    ), decimal_2_degrees(
        latlng[1], latitude=False, add_direction=add_direction
    )


def decimal_2_degrees(decimal, latitude=True, add_direction=False):
    """
    Converts a value in decimal degrees into a string with the format:
    DD:MM.SS (degrees:minutes.seconds).
    :param decimal: Decimal value to be converted.
    :param latitude: Determines whether the decimal degrees are for the
    latitude or for the longitude. This parameter is only necessary when it
    is required to add the direction at the end of the string (N, S, W, E).
    :param add_direction: If true, adds the direction for the DMS result.
    :return: The degrees in DMS format (with optional direction).
    """
    decimal = float(decimal)
    degrees = int(decimal)
    submin = abs((decimal - degrees) * 60)
    minutes = int(submin)
    subseconds = abs((submin - minutes) * 60)

    result = str(degrees) + ":" + str(minutes) + ":" +\
        "{0:.2f}".format(subseconds)

    if add_direction:
        if latitude:
            return result + "" + get_latitude_direction(degrees)
        else:
            return result + "" + get_longitude_direction(degrees)

    return result
