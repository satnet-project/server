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

from services.common import pusher as satnet_push

logger = logging.getLogger('network')


@decorators.every(minutes=5)
def keep_alive():
    """Push event
    Keep alive event that prevents remote sessions to automatically expire.
    """
    logger.info('Keep alive...')
    satnet_push.PushService().trigger_event(
        satnet_push.PushService.NETWORK_EVENTS_CHANNEL,
        satnet_push.PushService.KEEP_ALIVE,
        {'alive': True}
    )
    logger.info('keep alive sent!')
