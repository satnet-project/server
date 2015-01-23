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
from services.common.push import service as push_service
from services.leop.jrpc.serializers import messages as message_serializers

logger = logging.getLogger('leop')


class CommunicationsPush(object):
    """Push service
    Object that contains a set of static but convenient methods that facilitate
    the usage of the remote PUSH services.
    """

    @staticmethod
    def trigger_received_frame_event(message):
        """
        This method triggers the event about the reception of a new frame at
        the server. This way, the web clients can receive in real time the
        same frames that were received by the server.
        :param message: PassiveMessage object as read from the database
        """
        logger.info('PUSH frame event invoked!')
        push_service.PushService().trigger_event(
            push_service.PushService.DOWNLINK_CHANNEL,
            push_service.PushService.FRAME_EVENT,
            message_serializers.serialize_push_frame(message)
        )