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
angular.module('groundstation-models', [
    'marker-models'
]);

/**
 * Service that handles the configuration and map handlers/objects for all the
 * GroundStations.
 */
angular.module('groundstation-models').service('gs', [
    '$log', 'markers', function ($log, markers) {

        'use strict';

        /**
         * Configuration structure for all the GroundStations.
         * @type { { id: { marker: m, cfg: data } } }
         * @private
         */
        this.gsCfg = {};

        /**
         * Creates a confgiuration object using the values from the object
         * obtained from the SATNet server.
         * @param data The object as obtained from the SATNet server.
         * @returns {{
         *      id: (data.groundstation_id|*),
         *      callsign: (data.groundstation_callsign|*),
         *      latitude: *,
         *      longitude: *,
         *      elevation: (data.groundstation_elevation|*)
         *  }}
         */
        this.createCfg = function (data) {
            return {
                id: data.groundstation_id,
                callsign: data.groundstation_callsign,
                latitude: data.groundstation_latlon[0],
                longitude: data.groundstation_latlon[1],
                elevation: data.groundstation_elevation
            };
        };

        /**
         * Creates a new configuration object for the GroundStation based on the
         * information contained in the data structure.
         * @param data Information as retrieved through JSON-RPC from the server.
         * @returns {*} Leaflet.marker for this GroundStation.
         */
        this.add = function (data) {
            var id = data.groundstation_id;
            this.gsCfg[id] = {};
            this.gsCfg[id].cfg = this.createCfg(data);
            return markers.addGS(id, this.gsCfg[id]).then(function (data) {
                console.log(
                    '[gs-model] GS added, cfg = ' + JSON.stringify(data.cfg)
                );
            });
        };

        /**
         * Removes a given GroundStation from the system, erasing its information
         * from the configuration structure and all related markers.
         * @param id The identifier of the GroundStation to be removed.
         */
        this.remove = function (id) {
            if (this.gsCfg.hasOwnProperty(id) === false) {
                throw '[gs-model] No gs found, id= ' + id;
            }
            markers.removeGS(id).then(function (data) {
                $log.log('[gs-model] Marker layer removed, id = ' + data);
            });
            delete this.gsCfg[id];
            $log.log('[gs-model] GS removed, id = ' + id);
        };

        /**
         * Dirty check and update of the position of the GroundStation (both in
         * the configuration structure and in its marker).
         * @param gsId The identifier of the GroundStation.
         * @param data The new configuration for the GroundStation.
         * @private
         */
        this.latlngDirtyUpdate = function (gsId, data) {
            var llChanged = false,
                newLat = data.groundstation_latlon[0],
                newLng = data.groundstation_latlon[1],
                oldLat = this.gsCfg[gsId].cfg.latitude,
                oldLng = this.gsCfg[gsId].cfg.longitude;
            if (newLat !== oldLat) {
                llChanged = true;
            }
            if (newLng !== oldLng) {
                llChanged = true;
            }
            if (llChanged === true) {
                this.gsCfg[gsId].cfg.latitude = newLat;
                this.gsCfg[gsId].cfg.longitude = newLng;
                markers.updateGS(gsId, newLat, newLng);
            }
        };

        /**
         * Updates the configuration of a given GroundStation with the information
         * contained in the data parameter.
         * @param data Data structure as gathered from the JSON-RPC server.
         */
        this.configure = function (data) {
            var gsId = data.groundstation_id;
            if (!this.gsCfg.hasOwnProperty(gsId)) {
                $log.warn('[markers] No marker for gs, id= ' + gsId);
                return;
            }
            // Callsign and minimum contact elevation are directly updated.
            this.gsCfg[gsId].cfg.groundstation_callsign
                = data.groundstation_callsign;
            this.gsCfg[gsId].cfg.groundstation_elevation
                = data.groundstation_elevation;
            // LAT/LNG dirty check + update only if necessary. This way,
            // unnecessary marker's redrawings are avoided.
            this.latlngDirtyUpdate(gsId, data);
        };

        /**
         * Returns a human-readable representation of all the configurationes saved
         * in the main structure for the available GroundStation objects.
         * @returns {String} Human-readable string.
         */
        this.asString = function () {
            var gs = null, gsBuffer = '', buffer = '', id;
            for (id in this.gsCfg) {
                if (this.gsCfg.hasOwnProperty(id)) {
                    gs = this.gsCfg[id];
                    gsBuffer = '"id": ' + id + ', ' +
                        '"cfg": ' + JSON.stringify(gs.cfg);
                    buffer += gsBuffer + ';\n';
                }
            }
            return buffer;
        };

    }
]);