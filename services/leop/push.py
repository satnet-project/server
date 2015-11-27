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

from services.common import pusher as push_service
from services.leop.jrpc.serializers import launch as launch_serial
from services.leop.jrpc.serializers import messages as message_serializers

logger = logging.getLogger('leop')


class LaunchPush(object):
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
        push_service.PushService().trigger_event(
            push_service.PushService.LEOP_DOWNLINK_CHANNEL,
            push_service.PushService.FRAME_EVENT,
            message_serializers.serialize_push_frame(message)
        )

    @staticmethod
    def trigger_gss_assigned(launch_id, groundstations):
        """
        This method triggers the event that notifies to the connected clients
        that some new groundstations have been assigned to the related launch.
        :param launch_id: Identifier of the launch
        :param groundstations: Identifier of the groundstations assigned (array)
        """
        push_service.PushService().trigger_event(
            push_service.PushService.LEOP_EVENTS_CHANNEL,
            push_service.PushService.LEOP_GSS_UPDATED_EVENT,
            launch_serial.serialize_leop_id(launch_id)
        )

        for g in groundstations:

            push_service.PushService().trigger_event(
                push_service.PushService.LEOP_EVENTS_CHANNEL,
                push_service.PushService.LEOP_GS_ASSIGNED_EVENT,
                {
                    'launch_id': str(launch_id),
                    'groundstation_id': str(g)
                }
            )

    @staticmethod
    def trigger_gss_released(launch_id, groundstations):
        """
        This method triggers the event that notifies to the connected clients
        that some groundstations have been released from the related launch.
        :param launch_id: Identifier of the launch
        :param groundstations: Identifier of the groundstations assigned (array)
        """
        for g in groundstations:

            push_service.PushService().trigger_event(
                push_service.PushService.LEOP_EVENTS_CHANNEL,
                push_service.PushService.LEOP_GS_RELEASED_EVENT,
                {
                    'launch_id': str(launch_id),
                    'groundstation_id': str(g)
                }
            )

    @staticmethod
    def trigger_ufo_identified(launch_id, ufo_id, spacecraft_id):
        """
        This method triggers the event that marks the identification of a given
        UFO as a spacecraft.
        :param launch_id: Identifier of the Launch
        :param ufo_id: Identifier of the UFO.
        :param spacecraft_id: Identifier of the spacecraft linked to this UFO
        """
        push_service.PushService().trigger_event(
            push_service.PushService.LEOP_EVENTS_CHANNEL,
            push_service.PushService.LEOP_UFO_IDENTIFIED,
            {
                'launch_id': str(launch_id),
                'ufo_id': str(ufo_id),
                'spacecraft_id': str(spacecraft_id)
            }
        )

    @staticmethod
    def trigger_ufo_updated(launch_id, ufo_id, spacecraft_id):
        """
        This method triggers the event that marks the identification of a given
        UFO as a spacecraft.
        :param launch_id: Identifier of the Launch
        :param ufo_id: Identifier of the UFO
        :param spacecraft_id: Identifier of the spacecraft linked to this UFO
        """
        push_service.PushService().trigger_event(
            push_service.PushService.LEOP_EVENTS_CHANNEL,
            push_service.PushService.LEOP_UFO_UPDATED,
            {
                'launch_id': str(launch_id),
                'ufo_id': str(ufo_id),
                'spacecraft_id': str(spacecraft_id)
            }
        )

    @staticmethod
    def trigger_ufo_forgotten(launch_id, ufo_id, spacecraft_id):
        """
        This method triggers the event that marks to the clients that the
        server has <forgotten> about a given UFO as a spacecraft.
        :param launch_id: Identifier of the Launch
        :param ufo_id: Identifier of the UFO (matches spacecraft_id xxxx)
        :param spacecraft_id: Identifier of the Spacecraft
        """
        push_service.PushService().trigger_event(
            push_service.PushService.LEOP_EVENTS_CHANNEL,
            push_service.PushService.LEOP_UFO_FORGOTTEN,
            {
                'launch_id': str(launch_id),
                'ufo_id': str(ufo_id),
                'spacecraft_id': str(spacecraft_id)
            }
        )

    @staticmethod
    def trigger_leop_sc_updated(launch_id, launch_sc_id):
        """
        Triggers the transmission of the event that reports the update of the
        SC related directly with the cluster.
        :param launch_id: Identifier of the Launch
        :param launch_sc_id: Identifier of the Spacecraft for the cluster
        """
        push_service.PushService().trigger_event(
            push_service.PushService.LEOP_EVENTS_CHANNEL,
            push_service.PushService.LEOP_SC_UPDATED,
            {
                'launch_id': str(launch_id),
                'launch_sc_id': str(launch_sc_id)
            }
        )
