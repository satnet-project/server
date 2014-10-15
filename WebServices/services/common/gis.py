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

import json
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

    r = json.loads(
        urllib2.urlopen(geoplugin_ip + ip).read()
    )
    latitude = r['geoplugin_latitude']
    longitude = r['geoplugin_longitude']

    return latitude, longitude


__G_API_GEOCODE_URL__ = 'http://maps.googleapis.com/maps/api/geocode/'
__G_API_GEOCODE_OUTPUT__ = ['json', 'xml']


def get_region(latitude, longitude):
    """
    This method returns the formatted name of the country to which this
    position belongs to.
    :param latitude: The latitude for the given point.
    :param longitude: The longitude for the given point.
    :return: (country-long, country-short, region-long, region-short).
    """
    # noinspection PyDeprecation
    url = __G_API_GEOCODE_URL__\
          +__G_API_GEOCODE_OUTPUT__[0]\
          + '?latlng='\
          + str(latitude) + ',' + str(longitude)\
          + '&sensor=true'

    r = json.loads(
        urllib2.urlopen(

        ).read()
    )

    return r['results'][0]['address_components'][6]['long_name'],\
        r['results'][0]['address_components'][6]['short_name'],\
        r['results'][0]['address_components'][5]['long_name'], \
        r['results'][0]['address_components'][5]['short_name']

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
    # noinspection PyDeprecation
    r = json.loads(
        urllib2.urlopen(
            ___G_API_ALTITUDE_URL__
            + ___G_API_ALTITUDE_OUTPUT__[0]
            + '?locations='
            + str(latitude) + ',' + str(longitude)
        ).read()
    )
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


def decimal_2_degrees(decimal, latitude=True, add_direction=False):
    """
    Converts a value in decimal degrees into a string with the format:
    DD:MM.SS (degrees:minutes.seconds).
    :param decimal: Decimal value to be converted.
    :param latitude: Determines whether the decimal degrees are for the
    latitude or for the longitude. This parameter is only necessary when it
    is required to add the direction at the end of the string (N, S, W, E).
    :param add_direction: If true, adds the direction for the DMS result.
    :return: The input degrees in DMS format (with optional direction).
    """
    degrees = int(decimal)
    submin = abs((decimal - int(decimal)) * 60)
    minutes = int(submin)
    subseconds = abs((submin - int(submin)) * 60)

    result = str(degrees) + ":" + str(minutes) + ":" +\
        str(subseconds)[0:5]

    if add_direction:
        if latitude:
            return result + "" + get_latitude_direction(degrees)
        else:
            return result + "" + get_latitude_direction(degrees)

    return result
