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
angular.module('x-satnet-services', [
    'satnet-services', 'celestrak-services'
]);

/**
 * Service that defines the basic calls to the services of the SATNET network
 * through JSON RPC. It defines a common error handler for all the errors that
 * can be overriden by users.
 */
angular.module('x-satnet-services').service('xSatnetRPC', [
    '$q', 'satnetRPC', 'celestrak',
    function ($q, satnetRPC, celestrak) {

        'use strict';

        /**
         * Reads the configuration for all the GroundStation objects available
         * in the server.
         * @returns Promise that returns an array with the configuration
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
         * Reads the basic configuration for a given spacecraft using the
         * Satnet and the Celestrak services.
         * @param   {String} id Identifier of the spacecraft within the
         *                      Satnet network.
         * @returns Promise that returns the configuration object for this
         *          spacecraft.
         */
        this.readSCCfg = function (id) {
            return satnetRPC.rCall('sc.get', [id]).then(function (cfg) {
                var tleId = cfg.spacecraft_tle_id;
                console.log('>>> tle_id = ' + tleId);
                return celestrak.findTle(tleId).then(function (tleArray) {
                    console.log('>>> tleArray = ' + JSON.stringify(tleArray));
                    return {
                        id: cfg.spacecraft_id,
                        cfg: cfg,
                        tle: {
                            id: cfg.spacecraft_tle_id,
                            l1: tleArray[0].l1,
                            l2: tleArray[0].l2
                        }
                    };
                });
            });
        };

        /**
         * Reads the configuration for a given spacecraft, including the
         * estimated groundtrack.
         * @param scId The identifier of the spacecraft.
         * @returns Promise that resturns the Spacecraft configuration object.
         */
        this.readFullSCCfg = function (scId) {
            var xcfg = null,
                p = [
                    this.readSCCfg(scId),
                    satnetRPC.rCall('sc.getGroundtrack', [scId])
                ];
            return $q.all(p).then(function (results) {
                xcfg = results[0];
                xcfg.groundtrack = results[1];
                return xcfg;
            });
        };

    }
]);