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
from services.simulation.models import groundtracks as gt_models
from services.simulation.models import passes as pass_models

logger = logging.getLogger('simulation')


@decorators.daily()
def propagate_groundtracks():
    """Periodic task.
    This task updates the available groundtracks for the different registered
    Spacecraft.
    """
    logger.info('[DAILY] >>> Propagating groundtracks')
    gt_models.GroundTrack.objects.propagate_groundtracks()
    logger.info('> Propagated!')


@decorators.daily()
def propagate_passes():
    """Periodic task.
    This task updates the available groundtracks for the different registered
    Spacecraft.
    """
    logger.info('[DAILY] >>> Propagating passes')
    pass_models.PassSlots.objects.propagate_pass_slots()
    logger.info('> Propagated!')
