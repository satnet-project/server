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

from datetime import timedelta
import ephem

from common import misc
from common import gis


def create_spacecraft(l0, l1, l2):
    """
    Method to convert a Spacecraft object from the database into a PyEphem
    spacecraft that can be used with that same library for simulation purposes.
    :param l0: Line#0 of the TLE file.
    :param l1: Line#1 of the TLE file.
    :param l2: Line#2 of the TLE file.
    :return: The object that has to be used with the PyEphem library.
    :raises: ObjectDoesNotExist in case there is no cush tle_id in the database.
    """
    return ephem.readtle(str(l0), str(l1), str(l2))


def create_groundstation(ground_station):
    """
    Creates an PyEphem observer object with the data from a GroundStation
    object.
    :param ground_station: Object from where to take the data required
    :return: The configured PyEphem observer object
    """
    gs_observer = ephem.Observer()

    gs_observer.lat = gis.decimal_2_degrees(
        ground_station.latitude
    )
    gs_observer.lon = gis.decimal_2_degrees(
        ground_station.longitude
    )
    gs_observer.horizon = gis.decimal_2_degrees(
        ground_station.contact_elevation
    )

    gs_observer.elevation = ground_station.altitude

    return gs_observer


def ephem_date_2_utc_datetime(e_date):
    """
    Method that converts an Ephem.date object into a Python Datetime object
    located in the UTC timezone.
    :param e_date: The Ephem.date object to be converted.
    :return: The resulting Python UTC-aware Datetime object.
    """
    return misc.localize_datetime_utc(e_date.datetime())


def datetime_2_ephem_string(dt):
    """
    Converts a datetime object into a string that can be used as an input for
    the Ephem implementation of the Date object: 'yyyy/mm/dd hh:ii:ss'
    # ### Datetime object does not
    :param dt: Datetime object to be converted.
    :return: String to be used as an input for the date object.
    """
    if dt is None:
        dt = misc.get_today_utc()
    return dt.strftime("%Y/%m/%d %I:%M:%S")


def calculate_pass_slots(ground_station, spacecraft, availability_slots):
    """
    Calculates the passess for the given spacecraft over the ground_station,
    for all the availability slots included in the list.
    :param ground_station: The GroundStation object for PyEphem.
    :param spacecraft: The Spacecraft object for PyEphem.
    :param availability_slots: List of tuples with UTC DateTime objects
    defining the slots of availability.
    :return: A list with all the pass slots linked with the AvailabilitySlot
    that generated them.
    """
    pass_slots = []

    for a_slot_i in availability_slots:

        pass_slots.append((
            calculate_pass_slot(
                ground_station, spacecraft, a_slot_i[0], a_slot_i[1]
            ),
            a_slot_i[2]
        ))

    return pass_slots


def calculate_pass_slot(
        observer, body,
        start, end,
        minimum_slot_duration=timedelta(minutes=1)
):
    """
    Calculates the passes available for the given spacecraft in between the
    start and end dates.
    :param observer: The GroundStation object for PyEphem.
    :param body: The Spacecraft object for PyEphem.
    :param start: The datetime object (UTC) that defines the start of the
    simulation.
    :param end: The datetime object (UTC) that defines the end of the
    simulation.
    :return: List with the datetime objects (UTC) with the passess for
    the given Spacecraft over the given GroundStation
    :raises ephem.CircumpolarError: Raised whenever a pass for a given
    simulation is either always up or the satellite never shows up above the
    defined horizon.
    """
    pass_slots = []
    observer.date = datetime_2_ephem_string(start)
    last_end = start

    while last_end < end:

        tr, azr, tt, altt, ts, azs = observer.next_pass(body)
        body.compute(observer)

        dt_tr = misc.localize_datetime_utc(tr.datetime())
        dt_ts = misc.localize_datetime_utc(ts.datetime())

        if dt_tr > end:
            break

        if dt_ts > end:
            slot_end = end
        else:
            slot_end = dt_ts

        if (slot_end - dt_tr) > minimum_slot_duration:
            pass_slots.append((dt_tr, slot_end))

        observer.date = ts + ephem.minute
        last_end = misc.localize_datetime_utc(observer.date.datetime())

    return pass_slots