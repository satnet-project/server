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
from services.configuration.models import availability, tle

logger = logging.getLogger('configuration')


@decorators.daily()
def populate_slots():
    """Periodic task
    Task to be executed periodically for updating the pass slots with the
    following ones (3 days in advance). The addition of a new
    AvailabilitySlot triggers the automatic (through signal) addition of all
    the associated OperationalSlot; therefore, it is not necessary to update
    the OperationalSlots table.
    """
    logger.info('[DAILY] >>> Populating slots')
    availability.AvailabilitySlot.objects.propagate_slots()
    logger.info('> Populated!')


@decorators.daily()
def clean_slots():
    """Periodic task
    This task cleans all the old AvailabilitySlots from the database. Since
    the deletion of a given AvailabilitySlot triggers the deletion of the
    associated OperationalSlots, it is not necessary to clean the
    OperationalSlots table afterwards.
    """
    logger.info('[DAILY] >>> Cleaning slots')
    old_slots = availability.AvailabilitySlot.objects.filter(
        end__lte=misc.get_today_utc()
    )
    logger.info('> About to delete ' + str(len(old_slots)) + ' slots.')
    old_slots.delete()
    logger.info('> Deleted!')


@decorators.daily()
def update_tle_database():
    """Periodic task
    Task to be executed periodically for cleaning up all users whose activation
    key is expired and they did not complete still their registration process.
    """
    logger.info("Updating Celestrak TLE database, daily task execution!")
    tle.TwoLineElementsManager.load_celestrak()
    logger.info('Updated!')


@decorators.every(minutes=5)
def update_polysat_tles():
    """Periodic task
    Task to be executed periodically for updating the TLEs from Polysat
    database.
    """
    logger.info('Updating Polysat TLE database, every 5 minutes!')
    tle.TwoLineElementsManager.load_polysat()
    logger.info('Updated!')