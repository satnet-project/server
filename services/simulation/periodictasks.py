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
    logger.info('[DAILY] >>> Propagating groundtracks')

    try:
        gt_models.GroundTrack.objects.propagate()
    except Exception as ex:
        logger.warning(
            '[DAILY] >>> Exception while propagating groundtracks, ex = ' + str(
                ex
            )
        )

    logger.info('[DAILY] >>> DONE propagating groundtracks')


@decorators.daily()
def clean_groundtracks():
    """Periodic groundtracks cleanup
    """
    logger.info('[DAILY] >>> Cleaning groundtracks')

    try:
        gt_models.GroundTrack.objects.filter(
            timestamp__lt=misc.get_utc_timestamp(
                misc.get_now_utc()
            )
        ).delete()
    except Exception as ex:
        logger.warning(
            '[DAILY] >>> Exception while cleaning groundtracks, ex = ' + str(
                ex
            )
        )

    logger.info('[DAILY] >>> DONE cleaning groundtracks')


@decorators.daily()
def propagate_passes():
    """Periodic groundtracks propagation
    """
    logger.info('[DAILY] >>> Propagating passes')

    try:
        pass_models.PassSlots.objects.propagate()
    except Exception as ex:
        logger.warning(
            '[DAILY] >>>  Exception while propagating passes, ex = ' + str(
                ex
            )
        )

    logger.info('[DAILY] >>> DONE propagating groundtracks')


@decorators.daily()
def clean_passes():
    """Periodic groundtracks cleanup
    """
    logger.info('[DAILY] >>> Cleaning passes')

    try:
        pass_models.PassSlots.objects.filter(
            end__lt=misc.get_utc_timestamp(
                misc.get_now_utc()
            )
        ).delete()
    except Exception as ex:
        logger.warning(
            '[DAILY] >>>  Exception while cleaning passes, ex = ' + str(
                ex
            )
        )

    logger.info('[DAILY] >>> DONE cleaning passes')
