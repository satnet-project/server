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

:Author:
    Ricardo Tubio-Pardavila (rtubiopa@calpoly.edu)
"""
__author__ = 'rtubiopa@calpoly.edu'

from datetime import timedelta
import logging
logger = logging.getLogger(__name__)
from periodically.decorators import daily

from common import misc
from booking.models.operational import OperationalSlotsManager
from booking.models.tle import TwoLineElementsManager

@daily()
def update_tle_database():
    """
    Task to be executed periodically for cleaning up all users whose activation
    key is expired and they did not complete still their registration process.
    """
    logger.info("Updating TLE database, daily task execution!")
    TwoLineElementsManager.load_tles()

@daily()
def update_pass_slots():
    """
    Task to be executed periodically for updating the pass slots with the
    following ones (3 days in advance).
    """
    logger.info("Updating pass slots, daily task execution!")
    OperationalSlotsManager.populate_slots(
        start=misc.get_midnight()+timedelta(days=3),
        duration=timedelta(days=1)
    )