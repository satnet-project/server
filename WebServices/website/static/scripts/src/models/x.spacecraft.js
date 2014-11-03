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
    'satnet-services', 'celestrak-services', 'spacecraft-models'
]);

/**
 * Service that handles the configuration and map handlers/objects for all the
 * GroundStations.
 */
angular.module('x-spacecraft-models')
    .service('xsc', [
        '$log', '$q', 'satnetRPC', 'celestrak', 'sc',
    function($log, $q, satnetRPC, celestrak)
{

    'use strict';
    
    /**
     * Reads the configuration for all the GroundStation objects available
     * in the server.
     * @returns {$q} Promise that returns an array with the configuration
     *               for each of the GroundStation objects.
     */
    this.getAllCfgs = function() {
        return satnetRPC.rCall('sc.list', []).then(function (scs) {
            var p = [];
            angular.forEach (scs, function(scI) {
                p.push(satnetRPC.readSCCfg(scI));
            });
            return $q.all(p).then(function(results) {
                var cfgs = [];
                for ( var j = 0; j < results.length; j++ ) {
                    cfgs.push(results[j]);
                }
                return cfgs;
            });
        });
    };

    this._getAll = function() {
        this._getAllCfgs().then(function (cfgs) {
            var c = [];
            angular.forEach (cfgs, function(cfg) {
                c.push(cfg['spacecraft_id']);
            });
            return $q.all(celestrak.findTle(c));
        });
    };
    
    this.initAll = function() {
        this._readAll().then(function (cfgs) {
            angular.forEach(cfgs, function(cfg) {
                //celestrak.findTle(cfg['spacecraft_id']).then(tle)
            });
        });
    };

}]);