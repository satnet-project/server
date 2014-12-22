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
import pytz
import sys
import StringIO
import unicodedata
import socket


def get_fqdn(ip_address):
    """
    Function that transforms a given IP address into the associated FQDN name
    for that host.
    :param ip_address: IP address of the remote host.
    :return: FQDN name for that host.
    """
    return socket.gethostbyaddr(ip_address)


def get_fqdn_ip():
    """
    Function that returns the hostname as read from the socket library and
    the IP address for that hostname.
    :return: String with the name of the current host.
    """
    hn = 'localhost'
    try:
        hn = socket.getfqdn()
    except:
        pass

    return hn, socket.gethostbyname(hn)


def print_list(l, name=None, output=sys.stdout):
    """
    Function that prints the elements of a given list, one per line.
    :param l: The list to be printed out.
    """
    if len(l) == 0:
        print >> output, 'Empty list'
        return

    if name is None:
        name = str(l[0].__class__)

    print >> output, '>>>>>>> list = ' + name + ', len = ' + str(len(l))
    for l_i in l:
        print >> output, str(l_i)


def list_2_string(l, list_name='List'):
    """
    Function that prints the given list of elements into a string object.
    :param l: The list to be printed in the string
    :param list_name: The name for this list
    :return: String object with the list printed within
    """
    buff = StringIO.StringIO()
    print_list(l, name=list_name, output=buff)
    return buff.getvalue()


def print_dictionary(d, nested_level=0, output=sys.stdout, spacing='   '):
    """
    Function that recursively prints a dict and all its nested dictionaries.
    :param d: the dictionary to be printed.
    :param nested_level: used to increase the spacing for items in between
    nested dictionaries.
    :param output: the output where the function prints the data from the
    dictionaries.
    :param spacing: the string used as a base for spacing items in between
    dictionaries.
    """
    if type(d) == dict:
        print >> output, '%s{' % (nested_level * spacing)
        for k, v in d.items():
            if hasattr(v, '__iter__'):
                print >> output, '%s%s:' % ((nested_level + 1) * spacing, k)
                print_dictionary(v, nested_level + 1, output)
            else:
                print >> output, '%s%s: %s' % ((nested_level + 1) * spacing,
                                               k, v)
        print >> output, '%s}' % (nested_level * spacing)
    elif type(d) == list:
        print >> output, '%s[' % (nested_level * spacing)
        for v in d:
            if hasattr(v, '__iter__'):
                print_dictionary(v, nested_level + 1, output)
            else:
                print >> output, '%s%s' % ((nested_level + 1) * spacing, v)
        print >> output, '%s]' % (nested_level * spacing)
    else:
        print >> output, '%s%s' % (nested_level * spacing, d)


def dict_2_string(d):
    """
    Function that prints the elements of the given dictionary into a string
    object.
    :param d: The dictionary to be printed in the string
    :return: String object with the dictionary printed within
    """
    buff = StringIO.StringIO()
    print_dictionary(d, output=buff)
    return buff.getvalue()


def unicode_2_string(unicode_string):

    return unicodedata\
        .normalize('NFKD', unicode_string)\
        .encode('ascii', 'ignore')

def get_now_utc(no_microseconds=True):
    """
    This method returns now's datetime object UTC localized.
    :param no_microseconds=True: sets whether microseconds should be cleared.
    :return: the just created datetime object with today's date.
    """
    if no_microseconds:
        return pytz.utc.localize(datetime.datetime.utcnow()).replace(
            microsecond=0
        )
    else:
        return pytz.utc.localize(datetime.datetime.utcnow())


def get_now_hour_utc(no_microseconds=True):
    """
    This method returns now's hour in the UTC timezone.
    :param no_microseconds=True: sets whether microseconds should be cleared.
    :return: The time object within the UTC timezone.
    """
    if no_microseconds:
        return datetime.time.utcnow().replace(microsecond=0).time()
    else:
        return datetime.time.utcnow().time()


def get_today_utc():
    """
    This method returns today's date localized with the microseconds set to
    zero.
    :return: the just created datetime object with today's date.
    """
    return pytz.utc.localize(datetime.datetime.utcnow()).replace(
        hour=0, minute=0, second=0, microsecond=0
    )


def get_next_midnight():
    """
    This method returns today's datetime 00am.
    :return: the just created datetime object with today's datetime 00am.
    """
    return pytz.utc.localize(datetime.datetime.today()).replace(
        hour=0, minute=0, second=0, microsecond=0
    ) + datetime.timedelta(days=1)


def localize_date_utc(date):
    """
    Localizes in the UTC timezone the given date object.
    :param date: The date object to be localized.
    :return: A localized datetime object in the UTC timezone.
    """
    return pytz.utc.localize(
        datetime.datetime.combine(
            date, datetime.time(hour=0, minute=0, second=0)
        )
    )


def localize_datetime_utc(date_time):
    """
    Localizes in the UTC timezone a given Datetime object.
    :param date_time: The object to be localized.
    :return: Localized Datetime object in the UTC timezone.
    """
    return pytz.utc.localize(date_time)


def localize_time_utc(non_utc_time):
    """
    Localizes in the UTC timezone the given time object.
    :param non_utc_time: The time object to be localized.
    :return: A localized time object in the UTC timezone.
    """
    return pytz.utc.localize(non_utc_time)


TIMESTAMP_0 = localize_date_utc(datetime.datetime(year=1970, month=1, day=1))


def get_utc_timestamp(utc_datetime=None):
    """
    Returns a timestamp with the number of miliseconds ellapsed since January
    1st of 1970 for the given datetime object, UTC localized.
    :param utc_datetime: The datetime whose timestamp is to be calculated.
    :return: The number of miliseconds since 1.1.1970, UTC localized (integer)
    """
    if utc_datetime is None:
        utc_datetime = get_now_utc()
    diff = utc_datetime - TIMESTAMP_0
    return int(diff.total_seconds() * 10**6)