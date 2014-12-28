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

/** Module definition . */
angular.module('x-groundstation-models', [
    'broadcaster',
    'satnet-services',
    'x-satnet-services',
    'marker-models'
]);

/**
 * eXtended GroundStation models. Services built on top of the satnetRPC
 * service and the basic GroundStation models.
 */
angular.module('x-groundstation-models').service('xgs', [
    '$rootScope', 'broadcaster', 'satnetRPC', 'xSatnetRPC', 'markers',
    function ($rootScope, broadcaster, satnetRPC, xSatnetRPC, markers) {
        'use strict';

        /**
         * Initializes all the GroundStations reading the information from
         * the server. Markers are indirectly initialized.
         * @returns Promise that returns an array with all the
         *          configurations read.
         */
        this.initAll = function () {
            return xSatnetRPC.readAllGS().then(function (cfgs) {
                var gs_markers = [];
                angular.forEach(cfgs, function (cfg) {
                    gs_markers = gs_markers.concat(markers.createGSMarker(cfg));
                });
                return gs_markers;
            });
        };

        /**
         * Initializes all the GroundStations reading the information from
         * the server, for all those that are registered for this LEOP cluster.
         * Markers are indirectly initialized.
         * @returns Promise that returns an array with all the
         *          configurations read.
         */
        this.initAllLEOP = function () {
            return xSatnetRPC.readInUseLEOPGS($rootScope.leop_id)
                .then(function (cfgs) {
                    var gs_markers = [];
                    angular.forEach(cfgs, function (cfg) {
                        gs_markers = gs_markers.concat(
                            markers.createGSMarker(cfg)
                        );
                    });
                    return gs_markers;
                });
        };

        /**
         * Adds a new GroundStation together with its marker, using the
         * configuration object that it retrieves from the server.
         *
         * @param identifier Identififer of the GroundStation to be added.
         * @returns String Identifier of the just-created object.
         */
        this.add = function (identifier) {
            satnetRPC.rCall('gs.get', [identifier]).then(function (data) {
                return markers.createGSMarker(data);
            });
        };

        /**
         * Updates the markers for the given GroundStation object.
         * @param identifier Identifier of the GroundStation object.
         */
        this.update = function (identifier) {
            satnetRPC.rCall('gs.get', [identifier]).then(function (data) {
                return markers.updateGSMarker(data);
            });
        };

        /**
         * Removes the markers for the given GroundStation object.
         * @param identifier Identifier of the GroundStation object.
         */
        this.remove = function (identifier) {
            return markers.removeGSMarker(identifier);
        };

        /**
         * Private method that creates the event listeners for this service.
         */
        this.initListeners = function () {
            var self = this;
            $rootScope.$on(broadcaster.GS_ADDED_EVENT, function (event, id) {
                console.log(
                    '@on-gs-added-event, event = ' + event + ', id = ' + id
                );
                self.add(id);
            });
            $rootScope.$on(broadcaster.GS_REMOVED_EVENT, function (event, id) {
                console.log(
                    '@on-gs-removed-event, event = ' + event + ', id = ' + id
                );
                self.remove(id);
            });
            $rootScope.$on(broadcaster.GS_UPDATED_EVENT, function (event, id) {
                console.log(
                    '@on-gs-updated-event, event = ' + event + ', id = ' + id
                );
                self.update(id);
            });

        };

    }
]);