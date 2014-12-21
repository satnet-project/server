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
    '$q', 'satnetRPC', function ($q, satnetRPC) {

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
         * Reads the configuration for all the GroundStation objects available
         * in the server.
         * @returns Promise that returns an array with the configuration for
         *          each of the GroundStation objects.
         */
        this.readAllSCConfiguration = function () {
            return satnetRPC.rCall('sc.list', []).then(function (scs) {
                var p = [];
                angular.forEach(scs, function (sc) {
                    p.push(satnetRPC.readSCCfg(sc));
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
         * Reads the configuration for all the GroundStations associated with
         * this LEOP cluster.
         * @param leop_id Identifier of the LEOP cluster.
         * @returns {*} { leop_gs_available: [gs_cfg], leop_gs_inuse: [gs_cfg]}
         */
        this.readLEOPGSConfiguration = function (leop_id) {
            return satnetRPC.rCall('leop.gs.list', [leop_id])
                .then(function (gss) {
                    var p = [];
                    angular.forEach(gss.leop_gs_available, function (gs) {
                        p.push(satnetRPC.rCall('gs.get', [gs]));
                    });
                    angular.forEach(gss.leop_gs_inuse, function (gs) {
                        p.push(satnetRPC.rCall('gs.get', [gs]));
                    });
                    return $q.all(p).then(function (results) {
                        var a_cfgs = [], u_cfgs = [], j, r_j, r_j_id;
                        for (j = 0; j < results.length; j += 1) {
                            r_j = results[j];
                            r_j_id = r_j.groundstation_id;
                            if (gss.leop_gs_available.indexOf(r_j_id) >= 0) {
                                a_cfgs.push(r_j);
                            } else {
                                u_cfgs.push(r_j);
                            }
                        }
                        return {
                            leop_gs_available: a_cfgs,
                            leop_gs_inuse: u_cfgs
                        };
                    });
                });
        };

    }
]);