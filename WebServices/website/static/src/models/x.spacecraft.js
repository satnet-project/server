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
 * Created by rtubio on 10/28/14.
 */

/** Module definition (empty array is vital!). */
angular.module('x-spacecraft-models', [
    'broadcaster', 'satnet-services', 'x-satnet-services', 'marker-models'
]);

/**
 * eXtended GroundStation models. Services built on top of the satnetRPC
 * service and the basic Spacecraft models.
 */
angular.module('x-spacecraft-models').service('xsc', [
    '$rootScope',
    'broadcaster',
    'satnetRPC',
    'xSatnetRPC',
    'markers',
    function (
        $rootScope,
        broadcaster,
        satnetRPC,
        xSatnetRPC,
        markers
    ) {

        'use strict';

        /**
         * Initializes all the configuration objects for the available
         * spacecraft.
         * @returns {[Object]} Array with the configuration objects.
         */
        this.initAll = function () {
            return xSatnetRPC.readAllSC()
                .then(function (cfgs) {
                    var sc_markers = [];
                    angular.forEach(cfgs, function (cfg) {
                        sc_markers = sc_markers.concat(markers.addSC(cfg));
                    });
                    return sc_markers;
                });
        };

        /**
         * Initializes all the Spacecraft reading the information from the
         * server, for all those that are registered for this LEOP cluster.
         * Markers are indirectly initialized.
         * @returns Promise that returns an array with all the
         *          configurations read.
         */
        this.initAllLEOP = function () {
            return xSatnetRPC.readLEOPCluster($rootScope.leop_id)
                .then(function (cfgs) {
                    var cluster_markers = [];
                    angular.forEach(cfgs, function (cfg) {
                        cluster_markers = cluster_markers.concat(
                            markers.addSC(cfg)
                        );
                    });
                    return cluster_markers;
                });
        };

        /**
         * Adds a new Spacecraft together with its marker, using the
         * configuration object that it retrieves from the server.
         * @param identifier Identififer of the Spacecraft to be added.
         */
        this.addSC = function (identifier) {
            return satnetRPC.readSCCfg(identifier).then(function (data) {
                console.log('>> readSCCfg, data = ' + JSON.stringify(data));
                return markers.addSC(identifier, data);
            });
        };

        /**
         * Updates the configuration for a given Spacecraft.
         * @param identifier The identifier of the Spacecraft.
         */
        this.updateSC = function (identifier) {
            return satnetRPC.rCall('sc.get', [identifier])
                .then(function (data) { return markers.updateSC(data); });
        };

        /**
         * Removes the markers for the given Spacecraft.
         * @param identifier The identifier of the Spacecraft.
         */
        this.removeSC = function (identifier) {
            markers.removeSC(identifier).then(function (data) { return data; });
        };

        /**
         * Private method that inits the event listeners for this service.
         */
        this.initListeners = function () {
            var self = this;
            $rootScope.$on(broadcaster.SC_ADDED_EVENT, function (event, id) {
                console.log(
                    '@on-sc-added-event, event = ' + event + ', id = ' + id
                );
                self.addSC(id);
            });
            $rootScope.$on(broadcaster.SC_UPDATED_EVENT, function (event, id) {
                console.log(
                    '@on-sc-updated-event, event = ' + event + ', id = ' + id
                );
                self.updateSC(id);
            });
            $rootScope.$on(broadcaster.SC_REMOVED_EVENT, function (event, id) {
                console.log(
                    '@on-sc-removed-event, event = ' + event + ', id = ' + id
                );
                self.removeSC(id);
            });
        };

    }
]);