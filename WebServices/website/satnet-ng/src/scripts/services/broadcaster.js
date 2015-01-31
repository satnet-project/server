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
angular.module('broadcaster', ['pushServices']);

/**
 * Service used for broadcasting UI events in between controllers.
 */
angular.module('broadcaster').service('broadcaster', [
    '$rootScope', 'satnetPush',
    function ($rootScope, satnetPush) {

        'use strict';

        /**********************************************************************/
        /************************************************* INTERNAL CALLBACKS */
        /**********************************************************************/

        this.GS_ADDED_EVENT = 'gs.added';
        this.GS_REMOVED_EVENT = 'gs.removed';
        this.GS_UPDATED_EVENT = 'gs.updated';
        this.GS_AVAILABLE_ADDED_EVENT = 'gs.available.added';
        this.GS_AVAILABLE_REMOVED_EVENT = 'gs.available.removed';
        this.GS_AVAILABLE_UPDATED_EVENT = 'gs.available.updated';
        this.PASSES_UPDATED = 'passes.updated';
        this.LEOP_GSS_UPDATED_EVENT = 'leop.gss.updated';
        this.LEOP_GS_ASSIGNED_EVENT = 'leop.gs.assigned';
        this.LEOP_GS_RELEASED_EVENT = 'leop.gs.released';
        this.LEOP_UPDATED_EVENT = 'leop.updated';
        this.LEOP_FRAME_RX_EVENT = 'leop.frame.rx';

        /**
         * Function that broadcasts the event associated with the creation of a
         * new GroundStation available for the LEOP cluster.
         * @param identifier The identifier of the GroundStation.
         */
        this.gsAvailableAddedInternal = function (identifier) {
            $rootScope.$broadcast('gs.available.added', identifier);
        };

        /**
         * Function that broadcasts the event associated with the creation of a
         * new GroundStation.
         * @param identifier The identifier of the GroundStation.
         */
        this.gsAdded = function (identifier) {
            $rootScope.$broadcast(this.GS_ADDED_EVENT, identifier);
        };

        /**
         * Function that broadcasts the event associated with the removal of a
         * new GroundStation.
         * @param identifier The identifier of the GroundStation.
         */
        this.gsRemoved = function (identifier) {
            $rootScope.$broadcast(this.GS_REMOVED_EVENT, identifier);
        };

        /**
         * Function that broadcasts the event associated with the update of
         * new GroundStation.
         * @param identifier The identifier of the GroundStation.
         */
        this.gsUpdated = function (identifier) {
            $rootScope.$broadcast(this.GS_UPDATED_EVENT, identifier);
        };

        /**********************************************************************/
        /************************************************* INTERNAL CALLBACKS */
        /**********************************************************************/

        this.SC_ADDED_EVENT = 'sc.added';
        this.SC_REMOVED_EVENT = 'sc.removed';
        this.SC_UPDATED_EVENT = 'sc.updated';

        /**
         * Function that broadcasts the event associated with the creation of a
         * new Spacececraft.
         * @param identifier The identifier of the Spacececraft.
         */
        this.scAdded = function (identifier) {
            $rootScope.$broadcast(this.SC_ADDED_EVENT, identifier);
        };

        /**
         * Function that broadcasts the event associated with the removal of a
         * new Spacececraft.
         * @param identifier The identifier of the Spacececraft.
         */
        this.scRemoved = function (identifier) {
            $rootScope.$broadcast(this.SC_REMOVED_EVENT, identifier);
        };

        /**
         * Function that broadcasts the event associated with the update of
         * new Spacececraft.
         * @param identifier The identifier of the Spacececraft.
         */
        this.scUpdated = function (identifier) {
            $rootScope.$broadcast(this.SC_UPDATED_EVENT, identifier);
        };

        /**********************************************************************/
        /***************************************************** PUSH CALLBACKS */
        /**********************************************************************/

        this.gsAvailableAdded = function (id_object) {
            $rootScope.$broadcast('gs.available.added', id_object.identifier);
        };
        this.gsAvailableRemoved = function (id_object) {
            $rootScope.$broadcast('gs.available.removed', id_object.identifier);
            $rootScope.$broadcast('passes.updated', {});
        };
        this.gsAvailableUpdated = function (id_object) {
            $rootScope.$broadcast('gs.available.updated', id_object.identifier);
            $rootScope.$broadcast('passes.updated', {});
        };
        this.passesUpdated = function () {
            $rootScope.$broadcast('passes.updated', {});
        };
        this.scGtUpdated = function (data) {
            $rootScope.$broadcast('sc.updated', data.identifier);
        };
        this.leopGssUpdated = function (leop_id) {
            if ($rootScope.leop_id !== leop_id.identifier) {
                return;
            }
            $rootScope.$broadcast('leop.gss.updated', leop_id);
        };
        this.leopGsAssigned = function (data) {
            console.log('@broadcaster, ev = LEOP_GS_ASSIGNED, data = ' + JSON.stringify(data));
            if ($rootScope.leop_id !== data.launch_id) {
                return;
            }
            $rootScope.$broadcast('leop.gs.assigned', data.groundstation_id);
        };
        this.leopGsReleased = function (data) {
            console.log('@broadcaster, ev = LEOP_GS_RELEASED, data = ' + JSON.stringify(data));
            if ($rootScope.leop_id !== data.launch_id) {
                return;
            }
            $rootScope.$broadcast('leop.gs.released', data.groundstation_id);
        };
        this.leopUpdated = function (leop_id) {
            if ($rootScope.leop_id !== leop_id.identifier) {
                return;
            }
            $rootScope.$broadcast('leop.updated', leop_id);
        };
        this.leopUfoIdentified = function (data) {
            if ($rootScope.leop_id !== data.launch_id) { return; }
            $rootScope.$broadcast('sc.added', data.spacecraft_id);
            $rootScope.$broadcast('passes.updated', {});
        };
        this.leopUfoUpdated = function (data) {
            if ($rootScope.leop_id !== data.launch_id) { return; }
            $rootScope.$broadcast('sc.updated', data.spacecraft_id);
            $rootScope.$broadcast('passes.updated', {});
        };
        this.leopUfoForgot = function (data) {
            if ($rootScope.leop_id !== data.launch_id) { return; }
            $rootScope.$broadcast('sc.removed', data.spacecraft_id);
            $rootScope.$broadcast('passes.updated', {});
        };
        this.leopSCUpdated = function (data) {
            if ($rootScope.leop_id !== data.launch_id) { return; }
            $rootScope.$broadcast('sc.updated', data.launch_sc_id);
            $rootScope.$broadcast('passes.updated', {});
        };
        this.leopFrameReceived = function (data) {
            $rootScope.$broadcast('leop.frame.rx', data.frame);
        };
        this.leopFrameReceived = function (data) {
            $rootScope.$broadcast('keep.alive', {});
            console.log('ALIVE! data = ' + JSON.stringify(data));
        };

        satnetPush.bind(
            satnetPush.EVENTS_CHANNEL,
            satnetPush.GS_ADDED_EVENT,
            this.gsAvailableAdded,
            this
        );
        satnetPush.bind(
            satnetPush.EVENTS_CHANNEL,
            satnetPush.GS_REMOVED_EVENT,
            this.gsAvailableRemoved,
            this
        );
        satnetPush.bind(
            satnetPush.EVENTS_CHANNEL,
            satnetPush.GS_UPDATED_EVENT,
            this.gsAvailableUpdated,
            this
        );
        satnetPush.bind(
            satnetPush.SIMULATION_CHANNEL,
            satnetPush.PASSES_UPDATED_EVENT,
            this.passesUpdated,
            this
        );
        satnetPush.bind(
            satnetPush.SIMULATION_CHANNEL,
            satnetPush.GT_UPDATED_EVENT,
            this.scGtUpdated,
            this
        );
        satnetPush.bind(
            satnetPush.LEOP_CHANNEL,
            satnetPush.LEOP_UPDATED_EVENT,
            this.leopUpdated,
            this
        );
        satnetPush.bind(
            satnetPush.LEOP_CHANNEL,
            satnetPush.LEOP_GSS_UPDATED_EVENT,
            this.leopGssUpdated,
            this
        );
        satnetPush.bind(
            satnetPush.LEOP_CHANNEL,
            satnetPush.LEOP_GS_ASSIGNED_EVENT,
            this.leopGsAssigned,
            this
        );
        satnetPush.bind(
            satnetPush.LEOP_CHANNEL,
            satnetPush.LEOP_GS_RELEASED_EVENT,
            this.leopGsReleased,
            this
        );
        satnetPush.bind(
            satnetPush.LEOP_CHANNEL,
            satnetPush.LEOP_UFO_IDENTIFIED_EVENT,
            this.leopUfoIdentified,
            this
        );
        satnetPush.bind(
            satnetPush.LEOP_CHANNEL,
            satnetPush.LEOP_UFO_UPDATED_EVENT,
            this.leopUfoUpdated,
            this
        );
        satnetPush.bind(
            satnetPush.LEOP_CHANNEL,
            satnetPush.LEOP_UFO_FORGOTTEN_EVENT,
            this.leopUfoForgot,
            this
        );
        satnetPush.bind(
            satnetPush.LEOP_CHANNEL,
            satnetPush.LEOP_SC_UPDATED_EVENT,
            this.leopSCUpdated,
            this
        );
        satnetPush.bind(
            satnetPush.LEOP_DOWNLINK_CHANNEL,
            satnetPush.FRAME_EVENT,
            this.leopFrameReceived,
            this
        );
        satnetPush.bind(
            satnetPush.NETWORK_EVENTS_CHANNEL,
            satnetPush.KEEP_ALIVE,
            this.keepAliveReceived,
            this
        );

    }
]);