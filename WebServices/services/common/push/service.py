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
import pusher
from website import settings as satnet_cfg

logger = logging.getLogger('push')


class PushService(object):
    """Pusher object
    This class handles all the real-time communication events with the
    pusher.com webservice.
    """
    TEST_CHANNEL = 'test_channel'
    CONFIGURATION_EVENTS_CHANNEL = 'configuration.events.ch'
    SIMULATION_EVENTS_CHANNEL = 'simulation.events.ch'
    LEOP_EVENTS_CHANNEL = 'leop.events.ch'
    LEOP_DOWNLINK_CHANNEL = 'leop.downlink.ch'

    SATNET_CHANNELS = [
        TEST_CHANNEL,
        CONFIGURATION_EVENTS_CHANNEL,
        SIMULATION_EVENTS_CHANNEL,
        LEOP_EVENTS_CHANNEL,
        LEOP_DOWNLINK_CHANNEL
    ]

    TEST_EVENT = 'my_event'
    FRAME_EVENT = 'frameEv'
    GS_ADDED_EVENT = 'gsAddedEv'
    GS_REMOVED_EVENT = 'gsRemovedEv'
    GS_UPDATED_EVENT = 'gsUpdatedEv'
    PASSES_UPDATED_EVENT = 'passesUpdatedEv'
    GROUNDTRACK_UPDATED_EVENT = 'groundtrackUpdatedEv'
    LEOP_GSS_UPDATED_EVENT = 'leopGSsUpdatedEv'
    LEOP_UPDATED_EVENT = 'leopUpdatedEv'
    LEOP_UFO_IDENTIFIED = 'leopUFOIdentifiedEv'
    LEOP_UFO_UPDATED = 'leopUFOIdentifiedEv'
    LEOP_UFO_FORGOTTEN = 'leopUFOForgottenEv'
    LEOP_SC_UPDATED = 'leopSCUpdatedEv'

    # The puser object.
    _service = None
    # Dictionary with the channel objects available (keyed by name).
    _channels = {}

    def __init__(self):
        """Class constructor
        Initializes the communication with the pusher.com service. It relies on
        the configuration setup from the main website.settings file. It only
        initializes the object for the push service once, so different instances
        of this class might be using the same object. This way, it is not
        necessary to establish a new connection with the service provider.

        Apart from this, it also registers all the channels specified in the
        array: SATNET_CHANNELS
        """
        if not self._service:

            self._channels = {}
            self._service = pusher.Pusher(
                app_id=satnet_cfg.PUSHER_APP_ID,
                key=satnet_cfg.PUSHER_APP_KEY,
                secret=satnet_cfg.PUSHER_APP_SECRET
            )

            for channel in self.SATNET_CHANNELS:
                self.create_channel(channel)

    def get_push_service(self):
        """
        Basic method for accessing directly to the push service object.
        :return: The instance of the push service object currently being used
        """
        return self._service

    def test_service(self):
        """
        Method that uses the connection testing services of the pusher.com
        website.
        """
        self.trigger_event(
            self.TEST_CHANNEL, self.TEST_EVENT, {'message': 'TEST'}
        )

    def create_channel(self, name):
        """
        Creates a new channel with the given name.
        :param name: Name of the channel
        :return: Channel object directly invokable
        """
        if name in self._channels:
            raise Exception('Channel already exists, name = ' + str(name))

        channel = self._service[name]
        self._channels[name] = channel
        return name

    def remove_channel(self, name):
        """
        Removes an existing channel from the list of available ones.
        :param name: Name of the channel
        """
        if not name in self._channels:
            raise Exception('Channel does not exist, name = ' + str(name))

        del self._channels[name]

    def trigger_event(self, channel_name, event_name, data):
        """
        Triggers the remote execution of an event with the given data. Direct
        call to the "trigger" method of the pusher object interface.
        :param channel_name: Name of the channel
        :param event_name: Name of the event
        :param data: Data associated to this event
        """
        if not channel_name in self._channels:
            raise Exception(
                'Channel does not exist, name = ' + str(channel_name)
            )

        if satnet_cfg.TESTING:
            return

        logger.info(
            '[push] channel = <' + str(channel_name) +
            '>, event = <' + str(event_name) +
            '>, data = <' + str(data) + '>'
        )

        self._channels[channel_name].trigger(event_name, data)