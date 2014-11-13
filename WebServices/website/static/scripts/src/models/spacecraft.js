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
angular.module('spacecraft-models', [
    'marker-models'
]);

/**
 * Service that handles the configuration and map handlers/objects for all the
 * GroundStations.
 */
angular.module('spacecraft-models')
    .service('sc', [ '$log', 'markers', function ($log, markers) {

        'use strict';

        /**
         * Configuration structure for all the Spacecraft.
         * @type { { id: { marker: m, cfg: data } } }
         * @private
         */
        this.scCfg = {};

        /**
         * Creates a new configuration object for the Spacecraft based on the
         * information contained in the data structure.
         * @param data Information as retrieved through JSON-RPC from the server.
         * @returns {*} Leaflet.marker for this Spacecraft.
         */
        this.add = function (data) {
            var id = data.spacecraft_id;
            this.scCfg[id] = data;
            return markers.addSC(id, this.scCfg[id]).then(function (data) {
                console.log(
                    '[sc-model] New SC added, cfg = ' + JSON.stringify(data.cfg)
                );
            });
        };

        /**
         * Removes a given Spacecraft from the models layer.
         * @param id The identifier of the Spacecraft to be removed.
         */
        this.remove = function (id) {
            if (this.scCfg.hasOwnProperty(id) === false) {
                throw '[sc-model] No sc found, id= ' + id;
            }
            markers.removeSC(id).then(function (data) {
                $log.log('[sc-model] Marker layer removed, id = ' + data);
            });
            delete this.scCfg[id];
            $log.log('[sc-model] SC removed, id = ' + id);
        };

        /**
         * Initializes the internal variable with all the configuration
         * structures using the given structure.
         * @param {Object} cfgs All spacecraft configuration objects.
         */
        this.initAll = function (cfgs) {
            var i, c;
            for (i = 0; i < cfgs.length; i += 1) {
                c = cfgs[i];
                this.scCfg[c.id] = {
                    id: c.id,
                    cfg: c.cfg,
                    tle: c.tle,
                    gt: c.groundtrack,
                    marker: null
                };
            }
            return cfgs;
        };

        /**
         * Returns the information for all the spacecraft configurations hold
         * as a human-readable string.
         * @returns {String} Human-readable string.
         */
        this.asString = function () {
            var buffer = '', scBuffer = '', id, c;
            for (id in this.scCfg) {
                if (this.scCfg.hasOwnProperty(id)) {
                    c = this.scCfg[id];
                    scBuffer = '{ id: ' + c.id + ', ' +
                        'cfg: ' + JSON.stringify(c.cfg) + ', ' +
                        'tle: ' + JSON.stringify(c.tle) + ', ' +
                        'gt.length = ' + c.groundtrack.length + ' }';
                    buffer += scBuffer + ';\n';
                }
            }
            return buffer;
        };

    }]);