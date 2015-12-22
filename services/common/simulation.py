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
from datetime import timedelta as py_td
import ephem
import logging
import numpy
from services.common import gis, misc

logger = logging.getLogger('common')


class OrbitalSimulator(object):
    """
    This class holds all the methods necessary for the simulation of the
    passes of the Spacecraft over GroundStations.
    """

    # Flag that indicates whether the simulator should assume that it is
    # being used for a test and, therefore, return hard coded results. These
    # hard-coded results can be used instead of unpredictable slots and,
    # therefore, the behavior of the functions that depend on the results of
    # the simulations can be verified.
    _test_mode = False

    # Flag that indicates whether the invokation of one of the methods that
    # internally calls the routines for the actual mathematical simulations,
    # must raise an Exception instead of properly executing the method itself.
    _fail_test = False

    def set_debug(self, on=True, fail=False):
        """
        This method sets the OrbitalSimulator debug mode ON (on=True) or OFF
        (on=False). Default: on=True

        :param on: Flag that enables/disables the debug mode
        :param fail: Flag that triggers a simulated exception
        """
        self._test_mode = on
        self._fail_test = fail

    def get_debug(self):
        """Returns the debug flag for the Simulation object.
        :return: boolean debug flag.
        """
        return self._test_mode

    # Observer for the simulation (GroundStation simulation object).
    _observer = None
    # Body for the simulation (Spacecraft simulation object).
    _body = None
    # TLE in use for the simulation (taken from Spacecraft).
    _tle = None

    @staticmethod
    def normalize_string(l0, l1, l2):
        """Static method
        Normalizes the three parameters from unicode to string, in case it is
        necessary.
        :param l0: Line#0 of the TLE file
        :param l1: Line#1 of the TLE file
        :param l2: Line#2 of the TLE file
        :return: Tuple (l0, l1, l2)

        OLD encoding change from str to 'ascii', Python 2.7
        if isinstance(l0, str):
            l0 = unicodedata.normalize('NFKD', l0).encode('ascii', 'ignore')
        if isinstance(l1, str):
            l1 = unicodedata.normalize('NFKD', l1).encode('ascii', 'ignore')
        if isinstance(l2, str):
            l2 = unicodedata.normalize('NFKD', l2).encode('ascii', 'ignore')
        """

        if isinstance(l0, bytes):
            l0 = str(l0, 'ascii')
        if isinstance(l1, bytes):
            l1 = str(l1, 'ascii')
        if isinstance(l2, bytes):
            l2 = str(l2, 'ascii')

        return l0, l1, l2

    @staticmethod
    def check_tle_format(l0, l1, l2):
        """Static method
        Checks whether the format for a given TLE is correct or not.
        :param l0: Line#0 of the TLE file
        :param l1: Line#1 of the TLE file
        :param l2: Line#2 of the TLE file
        :return: True if the operation could succesuffly be completed
        """
        l0, l1, l2 = OrbitalSimulator.normalize_string(l0, l1, l2)
        ephem.readtle(l0, l1, l2)
        return True

    @staticmethod
    def _create_test_operational_slots(
        start, end, minimum_duration=datetime.timedelta(minutes=5)
    ):
        """
        Static method that creates the OperationalSlots to be used for
        testing purposes.
        :return: List with the testing OperationalSlots.
        """
        if start is None:
            now = misc.get_now_utc()
            return [(now, now + minimum_duration)]

        if end is None:
            return [(start, start + minimum_duration)]

        return [(start, end)]

    @staticmethod
    def ephem_date_2_utc_datetime(e_date):
        """
        Method that converts an Ephem.date object into a Python Datetime object
        located in the UTC timezone.
        :param e_date: The Ephem.date object to be converted.
        :return: The resulting Python UTC-aware Datetime object.
        """
        return misc.localize_datetime_utc(e_date.datetime())

    @staticmethod
    def datetime_2_ephem_string(dt):
        """
        Converts a datetime object into a string that can be used as an input
        for the Ephem implementation of the Date object: 'yyyy/mm/dd hh:ii:ss'
        # ### Datetime object does not
        :param dt: Datetime object to be converted.
        :return: String to be used as an input for the date object.
        """
        if dt is None:
            dt = misc.get_today_utc()
        return dt.strftime("%Y/%m/%d %H:%M:%S")

    @staticmethod
    def dbtle_2_ephem_str(spacecraft_tle):
        """
        Converts into the proper format required by the Ephem objects the TLE
        information contained in the database object.
        :param spacecraft_tle: TLE object from the database.
        :return: (name, line_1, line_2) in str format.
        """
        return misc.unicode_2_string(spacecraft_tle.identifier),\
            misc.unicode_2_string(spacecraft_tle.first_line),\
            misc.unicode_2_string(spacecraft_tle.second_line)

    def set_groundstation(self, groundstation):
        """
        Creates an PyEphem observer object with the data from a GroundStation
        object.
        :param groundstation: Object from where to take the data required
        """
        self._observer = ephem.Observer()
        self._observer.lat = gis.decimal_2_degrees(groundstation.latitude)
        self._observer.lon = gis.decimal_2_degrees(groundstation.longitude)
        self._observer.horizon = gis.decimal_2_degrees(
            groundstation.contact_elevation
        )
        self._observer.elevation = groundstation.altitude

    def set_spacecraft(self, spacecraft_tle):
        """
        Creates an PyEphem body object with the data from a Spacecraft object.
        :param spacecraft_tle: Spacecraft's tle as obtained by invoking the
        method "get" of the <services.configuration.models.TwoLineElement>.
        """
        self._tle = spacecraft_tle
        l0, l1, l2 = OrbitalSimulator.dbtle_2_ephem_str(spacecraft_tle)
        self._body = OrbitalSimulator.create_spacecraft(l0, l1, l2)

    @staticmethod
    def create_spacecraft(l0, l1, l2):
        """
        Method to convert a Spacecraft object from the database into a PyEphem
        spacecraft that can be used with that same library for simulation
        purposes.
        :param l0: Line#0 of the TLE file.
        :param l1: Line#1 of the TLE file.
        :param l2: Line#2 of the TLE file.
        :return: The object that has to be used with the PyEphem library.
        :raises: ObjectDoesNotExist in case there is no cush tle_id in the
        database.
        """
        l0, l1, l2 = OrbitalSimulator.normalize_string(l0, l1, l2)
        return ephem.readtle(l0, l1, l2)

    @staticmethod
    def get_update_duration():
        """Update window duration.
        This method returns the number of days for which the slots should be
        populated in the future.
        :return: Number of days as a datetime.timedelta object.
        """
        return datetime.timedelta(days=1)

    @staticmethod
    def get_update_window():
        """Population window slot.
        Static method that returns the time window for which the slots should
        be populated. Initially the slots should be populated from the end of
        the simulation window to N days after.
        :return: 2-tuple object with the start and the end of the window.
        """
        s_window = OrbitalSimulator.get_simulation_window()
        return (
            s_window[1],
            s_window[1] + OrbitalSimulator.get_update_duration()
        )

    @staticmethod
    def get_window_duration():
        """Simulation window duration.
        Static method that returns the duration of the window for the
        Simulation calculations of the slots.
        """
        return datetime.timedelta(days=3)

    @staticmethod
    def get_simulation_window():
        """Simulation window slot.
        Static method that returns the current 'in-use' simulation window,
        this is, the start and end datetime objects for the simulation of the
        slots that is currently being used.
        :return: Tuple (start, end) with the simulation window currently in
                use (UTC localized).
        """
        # From the 'window duration', 1 day has to be substracted (the day in
        #  course).
        start = misc.get_now_utc()
        end = misc.get_next_midnight()\
            + OrbitalSimulator.get_window_duration()\
            - datetime.timedelta(days=1)
        return start, end

    def calculate_passes(self, availability_slots):
        """
        Calculates the passess for the given spacecraft over the ground_station,
        for all the availability slots included in the list.
        :param availability_slots: List of tuples with UTC DateTime objects
        defining the slots of availability.
        :return: A list with all the pass slots linked with the AvailabilitySlot
        that generated them.
        """
        pass_slots = []

        for a_slot_i in availability_slots:

            pass_i = self.calculate_pass_slot(a_slot_i[0], a_slot_i[1])
            pass_i_id = a_slot_i[2]

            pass_slots.append((pass_i, pass_i_id))

        return pass_slots

    def calculate_pass_slot(
        self, start, end, minimum_slot_duration=datetime.timedelta(minutes=1)
    ):
        """
        Calculates the passes available for the given spacecraft in between the
        start and end dates.
        :param start: The datetime object (UTC) that defines the start of the
        simulation.
        :param end: The datetime object (UTC) that defines the end of the
        simulation.
        :param minimum_slot_duration: The minimum duration of a slot
        :return: List with the datetime objects (UTC) with the passess for
        the given Spacecraft over the given GroundStation
        :raises ephem.CircumpolarError: Raised whenever a pass for a given
        simulation is either always up or the satellite never shows up above the
        defined horizon.
        """
        if self._test_mode:
            if self._fail_test:
                raise Exception('TEST TEST TEST EXCEPTION')
            return OrbitalSimulator._create_test_operational_slots(start, end)

        pass_slots = []
        self._observer.date = OrbitalSimulator.datetime_2_ephem_string(start)
        last_end = start

        while last_end < end:

            tr, azr, tt, altt, ts, azs = self._observer.next_pass(self._body)
            self._body.compute(self._observer)

            if not tr or not ts:
                return pass_slots

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

            self._observer.date = ts + ephem.minute
            last_end = misc.localize_datetime_utc(
                self._observer.date.datetime()
            )

        return pass_slots

    @staticmethod
    def arrays_2_groundtrack(timestamps, latitudes, longitudes):
        """
        Converts the 3 oArrays into a single groundtrack array with objects as
        items.
        :param timestamps: array with the timestamps
        :param latitudes: array with the latitudes
        :param longitudes: array with the longitudes
        :return: Array where each element is { timestamp, latitude, longitude }.
                    The first timestamp is "start" and the last one is
                    "start+floor(duration/timestamp)*timestamp".
        """
        gt = []
        i = 0

        for ts_i in timestamps:

            lat_i = latitudes[i]
            lng_i = longitudes[i]

            gt.append({
                'timestamp': ts_i,
                'latitude': lat_i,
                'longitude': lng_i
            })

            i += 1

        return gt

    def calculate_groundtrack(
        self, spacecraft_tle,
        interval=None,
        timestep=py_td(seconds=20)
    ):
        """
        Calculates the GroundTrack for the spacecraft with the given tle object.
        :param spacecraft_tle: TLE for the spacecraft
        :param interval: simulation interval
        :param timestep: time ellapsed for the calculation of two subsequent
                            points in the ground track
        :return: Array where each element is { timestamp, latitude, longitude }.
                    The first timestamp is "start" and the last one is
                    "start+floor(duration/timestamp)*timestamp".
        """
        if not interval:
            interval = OrbitalSimulator.get_simulation_window()

        if self._test_mode:
            if self._fail_test:
                raise Exception('TEST TEST TEST EXCEPTION')

        self.set_spacecraft(spacecraft_tle)

        groundtrack = []
        date_i = interval[0]

        while date_i < interval[1]:

            self._body.compute(date_i)

            lat_i = numpy.rad2deg(self._body.sublat)
            lng_i = numpy.rad2deg(self._body.sublong)

            groundtrack.append({
                'timestamp': date_i,
                'latitude': lat_i,
                'longitude': lng_i
            })

            date_i += timestep

        return groundtrack

    def __unicode__(self):
        return '# ### Body (Spacecraft): ' + str(self._body)\
               + '\n* l0 = ' + self._tle.identifier\
               + '\n* l1 = ' + self._tle.first_line\
            + '\n* l2 = ' + self._tle.second_line\
            + '\n# ### Observer (Ground Station):'\
            + '\n* (lat, long) = (' + str(self._observer.lat) + ', '\
               + str(self._observer.lon) + ')'\
            + '\n* elevation = ' + str(self._observer.elevation)\
            + '\n* horizon = ' + str(self._observer.horizon)\
            + '\n* date = ' + str(self._observer.date)

    def __str__(self):
        return self.__unicode__()
