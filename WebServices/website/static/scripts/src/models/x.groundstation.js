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
angular.module(
    'x-groundstation-models',
    [
        'map-services', 'satnet-services', 'groundstation-models'
    ]
);

/**
 * eXtended GroundStation models. Services built on top of the satnetRPC
 * service and the basic GroundStation models.
 */
angular.module('x-groundstation-models')
    .service('xgs', [
        '$q', 'satnetRPC', 'gs', function ($q, satnetRPC, gs) {

            'use strict';

            /**
             * Reads the configuration for all the GroundStation objects available
             * in the server.
             * @returns {$q} Promise that returns an array with the configuration
             *               for each of the GroundStation objects.
             */
            this.readAllGSConfiguration = function () {
                return satnetRPC.rCall('gs.list', []).then(function (gss) {

                    var p = [];

                    angular.forEach(gss, function (gs) {
                        p.push(satnetRPC.rCall('gs.get', [gs]));
                    });

                    return $q.all(p).then(function (results) {
                        var cfgs = [], j;
                        for (j = 0; j < results.length; j += 1) {
                            cfgs.push(results[j]);
                        }
                        return cfgs;
                    });

                });
            };

            /**
             * Initializes all the GroundStations reading the information from
             * the server. Markers are indirectly initialized.
             * @returns {$q} Promise that returns an array with all the configurations
             *               read.
             */
            this.initAll = function () {
                return this.readAllGSConfiguration().then(function (gsCfgs) {
                    var p = [];
                    angular.forEach(gsCfgs, function (gsCfg) {
                        p.push(gs.create(gsCfg));
                    });
                    return $q.all(p).then(function (results) {
                        return results;
                    });
                });
            };

            /**
             * Updates the configuration for a given GroundStation.
             * @param gsId The identifier of the GroundStation.
             */
            this.updateGSMarker = function (gsId) {
                satnetRPC.rCall('gs.get', [gsId]).then(function (data) {
                    gs.configure(data);
                });
            };

        }]);