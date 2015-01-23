/**
 * Copyright 2014 Ricardo Tubio-Pardavila
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Created by rtubio on 10/24/14.
 */

/** Module definition (empty array is vital!). */
angular.module('pushServices', []);

/**
 * Service that defines the basic calls to the services of the SATNET network
 * through JSON RPC. It defines a common error handler for all the errors that
 * can be overriden by users.
 */
angular.module('satnet-services').service('satnetPush', [
    '$log', '$pusher',
    function ($log, $pusher) {
        'use strict';

        this._API_KEY = '79bee37791b6c60f3e56';

        this._client = null;
        this._service = null;

        // Names of the channels for subscription
        this.DOWNLINK_CHANNEL = 'downlink';
        this.EVENTS_CHANNEL = 'events';
        // List of events that an application can get bound to.
        this.FRAME_EVENT = 'frame';

        // List of channels that the service automatically subscribes to.
        this._channel_names = [
            'test_channel',
            this.DOWNLINK_CHANNEL,
            this.EVENTS_CHANNEL
        ];

        /**
         * Initializes the pusher service.
         * @private
         */
        this._init = function () {

            this._client = new Pusher(this._API_KEY);
            this._service = $pusher(this._client);
            this._service.connection.bind('state_change', this._logConnection);
            $log.info('[push] pusher.com service initialized!');

            this._subscribeChannels();

        };

        /**
         * Logs changes in the connection state for the pusher service.
         * @param states State changes
         * @private
         */
        this._logConnection = function (states) {
            $log.warn(
                '[push] State connection change, states = ' +
                    JSON.stringify(states)
            );
        };


        /**
         * Subscribe this service to all the channels whose names are part of
         * the "_channel_names_ array.
         * @private
         */
        this._subscribeChannels = function () {
            var self = this;
            angular.forEach(this._channel_names, function (name) {
                self._service.subscribe(name);
                $log.info('[push] Subscribed to channel <' + name + '>');
            });
        };

        /**
         * Method that binds the given function to the events triggered by
         * that channel.
         * @param channel_name Name of the channel
         * @param event_name Name of the event
         * @param callback_fn Function to be executed when that event happens
         */
        this.bind = function (channel_name, event_name, callback_fn) {
            if (!this._service.allChannels().hasOwnProperty(channel_name)) {
                throw 'Not subscribed to this channel, name = ' + channel_name;
            }
            this._service.channel(channel_name).bind(event_name, callback_fn);
        };

        this._init();

    }

]);