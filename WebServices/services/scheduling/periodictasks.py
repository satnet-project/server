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
from periodically import decorators

from services.common import misc
from services.scheduling.models import operational, tle

logger = logging.getLogger('scheduling')


@decorators.daily()
def update_operational_slots():
    """
    Task to be executed periodically for updating the pass slots with the
    following ones (3 days in advance).
    """
    logger.info("Populating OperationalSlots table, daily task execution!")
    operational.OperationalSlotsManager.populate_slots()


@decorators.daily()
def clean_operational_slots():
    """
    This task cleans all the old OperationalSlots from the database.
    """
    logger.info("Cleaning OperationalSlots table, daily task execution!")
    old_slots = operational.OperationalSlot.objects.filter(
        end__lte=misc.get_today_utc()
    )
    logger.info('> About to delete ' + len(old_slots) + ' OperationaSlots.')
    old_slots.delete()
    logger.info('> Deleted!')


@decorators.daily()
def update_tle_database():
    """
    Task to be executed periodically for cleaning up all users whose activation
    key is expired and they did not complete still their registration process.
    """
    logger.info("Updating TLE database, daily task execution!")
    tle.TwoLineElementsManager.load_tles()