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
    'x-groundstation-models', [
        'map-services', 'satnet-services', 'groundstation-models'
    ]
);

/**
 * eXtended GroundStation models. Services built on top of the satnetRPc
 * service and the basic GroundStation models.
 */
angular.module('x-groundstation-models').service('xgs', [
    'leafletData', 'maps', 'satnetRPC', 'gs',
    function(leafletData, maps, satnetRPC, gs)
{

    'use strict';

    /**
     * Initializes all the GroundStations reading the information from
     * the server. Markers are indirectly initialized.
     * @returns {$q} Promise that returns an array with all the configurations
     *               read.
     */
    this.initAll = function() {
        console.log('%%%%');
        return satnetRPC.readAllGSConfiguration().then(function(gsCfg) {
            var d = $q.defer(), p = [];
            console.log('...');
            for ( var i = 0; i < gsCfg.length; i++ ) {
                console.log('i = ' + i);
                p.push(gs.create(gsCfg));
            }
            $q.all(p).then(function (results) {
                console.log(' results = ' + JSON.stringify(results));
                return results;
            });
            return d.promise;
        });
    };

    /**
     * Updates the configuration for a given GroundStation.
     * @param gsId The identifier of the GroundStation.
     */
    this.updateGSMarker = function(gsId) {
        satnetRPC.call('gs.get', [gsId], function(data) {
            gs.configure(data);
        });
    };
}]);