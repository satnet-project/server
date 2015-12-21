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
from services.simulation.models import groundtracks as gt_models
from services.simulation.models import passes as pass_models

logger = logging.getLogger('simulation')


@decorators.daily()
def propagate_groundtracks():
    """Periodic groundtracks propagation
    """
    logger.info('>>> Populating groundtracks')

    try:
        gt_models.GroundTrack.objects.propagate()
    except Exception as ex:
        logger.warning('>>> Exception populating groundtracks, ex = ' + str(ex))
        return

    logger.info('>>> DONE propagating groundtracks')


@decorators.daily()
def clean_groundtracks(threshold=misc.get_now_utc()):
    """Periodic groundtracks cleanup
    @param threshold: datetime threshold to clean the old groundtracks
    """
    logger.info('>>> Cleaning groundtracks')

    try:

        no_deleted = gt_models.GroundTrack.objects.delete_older(
            threshold
        ).delete()
        logger.debug('>>> tasks@clean_passes.filtered = ' + str(no_deleted))

    except Exception as ex:

        logger.exception('>>> Exception cleaning groundtracks, ex = ' + str(ex))
        return

    logger.info('>>> DONE cleaning groundtracks')


@decorators.daily()
def propagate_passes():
    """Periodic groundtracks propagation
    """
    logger.info('>>> Propagating passes')

    try:
        pass_models.PassSlots.objects.propagate()
    except Exception as ex:
        logger.warning('>>> Exception propagating passes, ex = ' + str(ex))
        return

    logger.info('>>> DONE propagating groundtracks')


@decorators.daily()
def clean_passes(threshold=misc.get_now_utc()):
    """Periodic groundtracks cleanup
    Cleans the outdated passes from the database.
    @param threshold: datetime threshold to clean the old passes
    """
    logger.info('>>> Cleaning passes, threshold = ' + str(threshold))

    try:

        no_deleted = pass_models.PassSlots.objects.filter(
            end__lte=threshold
        ).delete()
        logger.debug('>>> tasks@clean_passes.filtered = ' + str(no_deleted))

    except Exception as ex:

        logger.exception('>>>  Exception cleaning passes, ex = ' + str(ex))
        return

    logger.info('>>> DONE cleaning passes')
