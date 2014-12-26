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
angular.module('x-groundstation-models', [
    'satnet-services',
    'x-satnet-services',
    'groundstation-models',
    'marker-models'
]);

/**
 * eXtended GroundStation models. Services built on top of the satnetRPC
 * service and the basic GroundStation models.
 */
angular.module('x-groundstation-models').service('xgs', [
    '$rootScope', '$q', 'satnetRPC', 'xSatnetRPC', 'gs', 'markers',
    function ($rootScope, $q, satnetRPC, xSatnetRPC, gs, markers) {
        'use strict';

        /**
         * Initializes all the GroundStations reading the information from
         * the server. Markers are indirectly initialized.
         * @returns Promise that returns an array with all the
         *          configurations read.
         */
        this.initAll = function () {
            return xSatnetRPC.readAllGSConfiguration()
                .then(function (cfgs) {
                    var p = [];
                    angular.forEach(cfgs, function (c) { p.push(gs.add(c)); });
                    return $q.all(p).then(function (r) { return r; });
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
            return xSatnetRPC.readAllLEOPGs($rootScope.leop_id)
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
         * @param id Identififer of the GroundStation to be added.
         */
        this.addGS = function (id) {
            satnetRPC.rCall('gs.get', [id]).then(function (data) {
                gs.add(data);
            });
        };

        /**
         * Updates the configuration for a given GroundStation.
         * @param id The identifier of the GroundStation.
         */
        this.updateGS = function (id) {
            satnetRPC.rCall('gs.get', [id]).then(function (data) {
                gs.configure(data);
            });
        };

    }
]);