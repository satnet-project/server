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
from datetime import datetime, timedelta
from pytz import utc as pytz_utc
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


def print_list(l, list_name='List'):
    """
    Function that prints the elements of a given list, one per line.
    :param l: The list to be printed out.
    """
    print '>>>>>>> PRINTING ' + list_name + ', len = ' + str(len(l))
    for l_i in l:
        print l_i


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


def define_interval(days=7):
    """
    Defines a tuple with the starting and ending dates for the interval
    of time that has to be used for the calculations of the available
    slots.
    :param days: Length of the interval for the calculations.
    :return: A tuple with the initial datetime and the final datetime for
    this interval.
    """
    utc_today = datetime.utcnow().date()
    begin_interval\
        = pytz_utc.localize(datetime(utc_today.year, utc_today.month,
                                     utc_today.day))
    end_interval = begin_interval + timedelta(days=days)
    return begin_interval, end_interval


def normalize_slots(slots):
    """
    This function "normalizes" a list of slots by merging all consecutive or
    overlapping slots into non-overlapping ones. IMPORTANT: the input slots
    array has to be sorted by initial datetime of the slot, this is, for a
    given slot at position 'i', it is always met the following condition:
    slots[i]['starting_date'] <= slots[i+1]['starting_date'].
    :param slots: The list of slots to be normalized.
    :return: The normalized list of slots.
    """

    if slots is None:
        return []

    n_slots = len(slots)
    if n_slots < 2:
        return n_slots

    n_list = []
    s = slots[0]
    t = slots[1]
    i = 0

    while i < n_slots:

#        print '### i = ' + str(i)\
#              + ', s = (' + s[0].isoformat() + ', ' + s[1].isoformat() + ')'\
#              + ', t = (' + t[0].isoformat() + ', ' + t[1].isoformat() + ')'
#        print '### n_list = ' + str(n_list)

        # CASE A: s < t, push(s) and next...
        if s[1] < t[0]:

#            print '>>> A'
            if s not in n_list:
                n_list.append(s)
            s = t

        # CASE B: s overlaps just a fraction of t.
        if (s[1] > t[0]) and (s[1] < t[1]):
#            print '>>> B, s[0] = ' + s[0].isoformat()\
#                  + ', t[1]' + t[1].isoformat()
            s = (s[0], t[1])
            if s not in n_list:
                n_list.append(s)

        # prepare next iteration
        if i > (n_slots - 2):
            if s not in n_list:
                n_list.append(s)
            break
        t = slots[i+1]
        i += 1

    return n_list


def merge_slots(p_slots, m_slots):
    """
    This function  merges the slots that define the availability of the
    ground station with the slots that define the non-availability of a
    ground station. The result are the actual availability slots.
    IMPORTANT: input lists of slots must be order by starting datetime.
    :param p_slots: The list of (+) slots.
    :param m_slots: The list of (-) slots.
    :return: Resulting list with the actual available slots.
    """

    if p_slots is None or m_slots is None:
        return []
    if len(p_slots) < 1:
        return []

    # Algorithm initialization
    slots = []
    p_next = True  # ### indicates whether the 'p' vector has to be updated
    p_n = len(p_slots)
    p_i = 0
    m_i = 0
    m_n = len(m_slots)
    if m_n > 0:
        m = m_slots[0]
        m_i = 1
    else:
        # All slots will be generated from today on, so this will be the
        # "oldest" slot independently of the rest...
        m = (datetime.today().replace(microsecond=0) - timedelta(days=1),
             datetime.today().replace(microsecond=0) - timedelta(days=1))

    # The algorithm is executed for all the add slots, since negative slots
    # do not generate actual slots at all, they only limit the range of the
    # add slots.
    while True:

        if p_next:
            if p_i == p_n:
                break
            p = p_slots[p_i]
            p_i += 1
        else:
            p_next = True

        if p[1] <= m[0]:
            # ### CASE A:
            slots.append(p)
            continue

        if p[0] >= m[1]:
            # ### CASE F:
            if m_i < m_n:
                m = m_slots[m_i]
                m_i += 1
            else:
                slots.append(p)
            continue

        if p[0] < m[0]:

            if (p[1] > m[0]) and (p[1] <= m[1]):
                # ### CASE B:
                slots.append((p[0], m[0]))
            if p[1] > m[1]:
                # ### CASE C:
                slots.append((p[0], m[0]))
                p = (m[1], p[1])
                p_next = False

        else:

            # ### CASE D:
            if p[1] > m[1]:
                p = (m[1], p[1])
                p_next = False
                if m_i < m_n:
                    m = m_slots[m_i]
                    m_i += 1

    return slots
