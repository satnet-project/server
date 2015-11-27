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
import logging
from django.db import models
from djorm_pgarray import fields as pgarray_fields
from services.common import simulation as simulator, misc
from services.configuration.models import segments as segment_models
from services.configuration.models import tle as tle_models

logger = logging.getLogger('simulation')


class GroundTrackManager(models.Manager):
    """
    Manager for the GroundTracks that handles the creation, update and deletion
    process of these objects from the database.
    """

    def create(self, spacecraft):
        """
        Creates a new GroundTrack object within the database for the spacecraft
        that has the given TLE. If the groundtrack already exists, it does not
        update it.
        :param spacecraft: Reference to the Spacecraft object.
        :return: Reference to the newly created object.
        """
        gt = simulator.OrbitalSimulator().calculate_groundtrack(spacecraft.tle)
        ts, lat, lng = GroundTrackManager.groundtrack_to_dbarray(gt)

        return super(GroundTrackManager, self).create(
            timestamp=ts, latitude=lat, longitude=lng,
            spacecraft=spacecraft, tle=spacecraft.tle
        )

    @staticmethod
    def remove_old(groundtrack):
        """
        Removes the old points of the groundtrack that are not applicable
        anymore. The results are not saved to the database.
        :param groundtrack: The groundtrack to be updated.
        :return: The updated groundtrack object.
        """
        now_ts = misc.get_utc_timestamp(
            misc.get_now_utc() + datetime.timedelta(seconds=1)
        )

        ts_l = groundtrack.timestamp
        la_l = groundtrack.latitude
        lo_l = groundtrack.longitude
        _2_remove = 0

        for ts in ts_l:
            if ts <= now_ts:
                _2_remove = ts_l.index(ts) + 1
            else:
                break

        groundtrack.timestamp = ts_l[_2_remove:]
        groundtrack.latitude = la_l[_2_remove:]
        groundtrack.longitude = lo_l[_2_remove:]

        return groundtrack

    @staticmethod
    def append_new(groundtrack, new_ts, new_lat, new_lng):
        """
        Appends the new points to the existing groundtrack. It does not save
        the results in the database.

        :param groundtrack: The groundtrack to be updated.
        :param new_ts: The new timestamps to be appended
        :param new_lat: The new latitudes to be appended
        :param new_lng: The new longitudes to be appended
        :return: The updated groundtrack object
        """
        ts_l = groundtrack.timestamp
        la_l = groundtrack.latitude
        lo_l = groundtrack.longitude

        groundtrack.timestamp = ts_l + new_ts
        groundtrack.latitude = la_l + new_lat
        groundtrack.longitude = lo_l + new_lng

        return groundtrack

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

            timestamps.append(
                misc.get_utc_timestamp(point['timestamp'])
            )
            latitudes.append(point['latitude'])
            longitudes.append(point['longitude'])

        return timestamps, latitudes, longitudes

    def propagate(self):
        """
        This method propagates the points for the GroundTracks along the
        update window. This propagation should be done after the new TLE's
        had been received.
        """
        os = simulator.OrbitalSimulator()
        (start, end) = os.get_update_window()

        logger.info('window = (' + str(start) + ', ' + str(end) + ')')

        for gt in self.all():

            if gt.timestamp:
                logger.info('gt.len (BEFORE) = ' + str(gt))
            else:
                logger.info('gt.len is empty')

            # 1) remove old groundtrack points
            gt = GroundTrackManager.remove_old(gt)

            try:

                # 2) new groundtrack points
                new_gt = os.calculate_groundtrack(
                    spacecraft_tle=gt.tle, start=start, end=end
                )
                ts, lat, lng = GroundTrackManager.groundtrack_to_dbarray(new_gt)
                # 3) create and store updated groundtrack
                gt = GroundTrackManager.append_new(gt, ts, lat, lng)
                # 4) the updated groundtrack is saved to the database.
                gt.save()

                if gt:
                    logger.info('gt.len (AFTER) = ' + str(gt))
                else:
                    logger.info('[@propagate_groundtracks] gt is None')

            except Exception as ex:

                logger.warning(
                    'Error while propagating groundtrack = ' + str(gt) +
                    'ex = ' + str(ex)
                )


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

    latitude = pgarray_fields.FloatArrayField(
        verbose_name='Latitude for the points of the GroundTrack'
    )
    longitude = pgarray_fields.FloatArrayField(
        verbose_name='Longitude for the points of the GroundTrack'
    )
    timestamp = pgarray_fields.BigIntegerArrayField(
        verbose_name='UTC time at which the spacecraft is going to pass over '
                     'this point'
    )

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
