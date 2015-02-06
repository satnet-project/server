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

import logging
from services.common.push import service as satnet_push

logger = logging.getLogger('simulation')


class SimulationPush(object):
    """Push service
    Object that contains a set of static but convenient methods that facilitate
    the usage of the remote PUSH services.
    """

    @staticmethod
    def trigger_passes_updated_event():
        """
        Triggers the transmission of this event through the pusher.com service.
        """
        satnet_push.PushService().trigger_event(
            satnet_push.PushService.SIMULATION_EVENTS_CHANNEL,
            satnet_push.PushService.PASSES_UPDATED_EVENT,
            {}
        )

    @staticmethod
    def trigger_gt_updated_event(spacecraft_id):
        """
        Triggers the transmission of this event through the pusher.com service.
        """
        satnet_push.PushService().trigger_event(
            satnet_push.PushService.SIMULATION_EVENTS_CHANNEL,
            satnet_push.PushService.GROUNDTRACK_UPDATED_EVENT,
            {'identifier': str(spacecraft_id)}
        )