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
angular.module('spacecraft-models', [ 'satnet-services' ]);

/**
 * Service that handles the configuration and map handlers/objects for all the
 * GroundStations.
 */
angular.module('spacecraft-models').service('sc', [
    '$rootScope', '$log', '$q', 'satnetRPC',
    function($rootScope, $log, $q, satnetRPC) {

        /**
         * Configuration structure for all the Spacecraft.
         * @type { { id: { marker: m, cfg: data } } }
         * @private
         */
        this._scCfg = {};

        this._readCfg = function(scId) {
            satnetRPC.rCall('sc.get', [scId]).then(
                function(result) {
                    var raw_cfg = result['data'];
                    var sc_id = raw_cfg['spacecraft_id'];
                    var sc_cfg = {};
                    var ll = L.latLng(42.6000, -8.9330);
                    var icon = L.icon({
                        iconUrl: '/static/images/icons/sc-icon.svg',
                        iconSize: [30, 30]
                    });
                    var m = L.marker(
                        ll, { draggable: false, icon: icon }
                    ).bindLabel(sc_id, { noHide: true });
                    return sc_cfg[sc_id] = {
                        'marker': m,
                        'config': {
                            'tleid': raw_cfg['spacecraft_tleid'],
                            'callsign': raw_cfg['spacecraft_callsign']
                            }
                    };
                }
            )
        };

        this._readAll = function() {
            return satnetRPC.rCall('sc.list', []).then(function(result) {
                console.log('XXXX data = ' + JSON.stringify(result));
                return result['data'];
            });
        };

        this._initList = function (list) {

            var defer = $q.defer();
            var promises = [];

            for ( var i = 0; i < list.length; i++ ) {
                promises.push(this._readCfg(list[i]));
            }

            $q.all(promises).then(function(result) {
                return result[0]['data'].slice(0);
            });

            return defer;
        };

        this.init = function() {
            this._readAll().then(function(list) { return this._initList(list); })
        };

    }
]);
