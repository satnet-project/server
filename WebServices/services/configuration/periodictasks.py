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
from services.configuration.models import availability

logger = logging.getLogger('configuration')


@decorators.daily()
def populate_slots():
    """
    Task to be executed periodically for updating the pass slots with the
    following ones (3 days in advance). The addition of a new
    AvailabilitySlot triggers the automatic (through signal) addition of all
    the associated OperationalSlot; therefore, it is not necessary to update
    the OperationalSlots table.
    """
    logger.info('[DAILY] >>> Populating slots')
    availability.AvailabilitySlot.objects.propagate_slots()

@decorators.daily()
def clean_slots():
    """
    This task cleans all the old AvailabilitySlots from the database. Since
    the deletion of a given AvailabilitySlot triggers the deletion of the
    associated OperationalSlots, it is not necessary to clean the
    OperationalSlots table afterwards.
    """
    logger.info('[DAILY] >>> Cleaning slots')
    old_slots = availability.AvailabilitySlot.objects.filter(
        end__lte=misc.get_today_utc()
    )
    logger.info('> About to delete ' + len(old_slots) + ' slots.')
    old_slots.delete()
    logger.info('> Deleted!')