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
    'x-groundstation-models', [ 'satnet-services', 'groundstation-models' ]
);

/**
 * eXtended GroundStation models. Services built on top of the satnetRPc
 * service and the basic GroundStation models.
 */
angular.module('x-groundstation-models').service('xgs', [
    '$rootScope', 'satnetRPC', 'gs', function($rootScope, satnetRPC, gs) {

    /**
     * Adds a marker to a given GroundStation.
     * @param gs_id Identifier of the GroundStation.
     */
    this.addGSMarker = function(gs_id) {
        satnetRPC.call('gs.get', [gs_id], function(data) {
            gs.create(data).addTo($rootScope._map);
        });
    };

    /**
     * Initializes the markers for all the GroundStations available at the
     * remote server.
     */
    this.initGSMarkers = function() {
        satnetRPC.call('gs.list', [], function(data) {
            for ( var i = 0; i < data.length; i++ ) {
                satnetRPC.call('gs.get', [data[i]], function(data) {
                    gs.create(data).addTo($rootScope._map);
                });
            }
        });
    };

    /**
     * Updates the configuration for a given GroundStation.
     * @param gs_id The identifier of the GroundStation.
     */
    this.updateGSMarker = function(gs_id) {
        satnetRPC.call('gs.get', [gs_id], function(data) {
            gs.configure(data);
        });
    };
}]);