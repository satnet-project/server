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

import bisect
from datetime import datetime as py_dt
from datetime import timedelta as py_td
from django.db import models
import logging
import json

from services.common import simulation, misc, slots as sn_slots
from services.configuration.models import segments as segment_models
from services.configuration.models import tle as tle_models


logger = logging.getLogger('simulation')


class GroundTrackManager(models.Manager):
    """
    Manager for the GroundTracks that handles the creation, update and deletion
    process of these objects from the database.
    """

    MAX_LLT_LENGTH = 10000000

    def create(self, spacecraft):
        """
        Creates a new GroundTrack object within the database for the spacecraft
        that has the given TLE. If the groundtrack already exists, it does not
        update it.
        :param spacecraft: Reference to the Spacecraft object.
        :return: Reference to the newly created object.
        """
        gt = simulation.OrbitalSimulator().calculate_groundtrack(spacecraft.tle)
        ts, lat, lng = GroundTrackManager.groundtrack_to_dbarray(gt)

        return super(GroundTrackManager, self).create(
            timestamp=ts, latitude=lat, longitude=lng,
            spacecraft=spacecraft, tle=spacecraft.tle
        )

    @staticmethod
    def groundtrack_to_dbarray(groundtrack):
        """
        Static method that transforms a groundtrack array composed by points
        (lat, lng, timestamp) into three independent oArrays that can be stored
        directly in a PostGres database.

        :param groundtrack: The groundtrack to be split
        :return: ([latitude], [longitude], [timestamp]), three independent
            oArrays with the components of a given point from the groundtrack
        """
        latitudes = []
        longitudes = []
        timestamps = []

        for point in groundtrack:

            timestamps.append(point['timestamp'].timestamp())
            latitudes.append(point['latitude'])
            longitudes.append(point['longitude'])

        return timestamps, latitudes, longitudes

    def delete_older(self, threshold=misc.get_now_utc()):
        """Filtering order
        This method implements the filtering for groundtrack timestamps older
        than the given threshold.

        TODO :: get rid of djorm_pgarray

        :param threshold: Threshold for the filter
        :return: Number of elements deleted from the database
        """
        no_deleted = 0

        for gt in self.all():

            ts_l, la_l, lo_l = gt.read()

            logger.info(
                '>>> @groundtracks.delete_older, gt.sc = ' + str(
                    gt.spacecraft.identifier
                )
            )

            if not ts_l:
                logger.info('>>> @groundtracks.delete_older, EMPTY GT')
                continue

            index = bisect.bisect_left(ts_l, threshold.timestamp())
            gt.write(ts_l[index:], la_l[index:], lo_l[index:])
            no_deleted += index

        return no_deleted

    def propagate(
        self,
        interval=simulation.OrbitalSimulator.get_update_window(),
        threshold=py_td(days=1)
    ):
        """
        This method propagates the points for the GroundTracks along the
        update window. This propagation should be done after the new TLE's
        had been received.

        @param interval: interval for the propagation
        @param threshold: timedelta interval during which no GT is propagated
        """
        logger.info(
            '>>> @groundtracks.propagate.interval = ' + sn_slots.string(
                interval
            )
        )

        for gt in self.all():

            ts_l, la_l, lo_l = gt.read()

            logger.info(
                '>>> @groundtracks.propagate, gt.sc = ' + str(
                    gt.spacecraft.identifier
                )
            )

            if not ts_l:
                logger.info('>>> @groundtracks.propagate, EMPTY GT')
                continue

            dt_ts = misc.localize_date_utc(py_dt.fromtimestamp(ts_l[-1]))
            diff = py_td(seconds=abs((dt_ts - interval[0]).total_seconds()))

            if diff < threshold:
                logger.info('>>> @groundtracks.propagate, THRESHOLD')
                continue

            try:

                new_gt = simulation.OrbitalSimulator().calculate_groundtrack(
                    spacecraft_tle=gt.tle, interval=interval
                )
                ts, lat, lng = GroundTrackManager.groundtrack_to_dbarray(new_gt)
                gt.append(ts, lat, lng)

            except Exception as ex:
                logger.exception('Error propagating groundtrack, ex = ' + str(
                    ex
                ))


class GroundTrack(models.Model):
    """
    Class that represents a GroundTrack for a given Spacecraft over the next
    simulation period.
    """
    class Meta:
        app_label = 'simulation'

    objects = GroundTrackManager()

    spacecraft = models.ForeignKey(
        segment_models.Spacecraft,
        unique=True,
        verbose_name='Reference to the Spacecraft that owns this GroundTrack'
    )

    tle = models.ForeignKey(
        tle_models.TwoLineElement,
        verbose_name='Reference to the TLE object used for this GroundTrack'
    )

    latitude = models.TextField(
        default='',
        max_length=GroundTrackManager.MAX_LLT_LENGTH,
        verbose_name='List of latitudes in a comma separated value'
    )
    longitude = models.TextField(
        default='',
        max_length=GroundTrackManager.MAX_LLT_LENGTH,
        verbose_name='List of longitudes in a comma separated value'
    )
    timestamp = models.TextField(
        default='',
        max_length=GroundTrackManager.MAX_LLT_LENGTH,
        verbose_name='List of timestamps in a comma separated value'
    )

    def append(self, timestamps, latitudes, longitudes):
        """
        Appends the new points to the existing groundtrack. It does not save
        the results in the database.

        :param timestamps: The new timestamps to be appended
        :param latitudes: The new latitudes to be appended
        :param longitudes: The new longitudes to be appended
        :return: The updated groundtrack object
        """
        tss, las, lns = self.read()

        # If the list is not empty, we have to check whether the new simulated
        # points are already included in the list. The latter condition is met
        # whenever the last element of the already stored list is not smaller
        # than the first element of the new groundtrack points (both list are
        # sored in terms of timestamps).
        if tss and not(tss[-1] < timestamps[0]):

            # With the bisect algorithm (dichotomy) we find the position of the
            # first element that is bigger than the given timestamp, that is,
            # the position of the new timestamp array that can be appended to
            # the existing groundtrack.
            position = bisect.bisect_left(timestamps, tss[-1])

            # The arrays are corrected in consequence
            timestamps = timestamps[position:]
            latitudes = latitudes[position:]
            longitudes = longitudes[position:]

        self.write(tss + timestamps, las + latitudes, lns + longitudes)

    def read(self):
        """
        Returns the groundtrack as a tuple of float arrays.
        :return: 3-tuple of float arrays, (timestamp, latitude, longitud)
        """
        return (
            json.loads(self.timestamp),
            json.loads(self.latitude),
            json.loads(self.longitude)
        )

    def write(self, timestamps, latitudes, longitudes):
        """
        Writes the given arrays of floats into the database as GroundTrack
        objects. It uses "json.dumps()" to dump it out as a string in a
        TextField within the database object.

        :param timestamps: Array of floats
        :param latitudes: Array of floats
        :param longitudes: Array of floats
        """
        self.timestamp = json.dumps(timestamps)
        self.latitude = json.dumps(latitudes)
        self.longitude = json.dumps(longitudes)
        self.save()

    def len(self):
        """
        Returns the length of the groundtrack - just a convenience method.
        :return: Number of points of the groundtrack
        """
        tss, las, lns = self.read()
        return len(tss)

    def __unicode__(self):
        """Unicode
        Returns a unicode representation of the state of this object.
        :return: Unicode string
        """
        result = '>>> groundtrack object, info = '\
            + 'sc.id = ' + str(self.spacecraft.identifier) + '\n'\
            + 'tle.id = ' + str(self.tle.identifier) + '\n'

        if self.timestamp:
            ts = 'timestamp = ' + str(self.timestamp)
            result += ts

        return result

    def __str__(self):
        """To String
        :return: Human readable string of the object
        """
        return self.__unicode__()
