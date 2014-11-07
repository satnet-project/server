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
angular.module('groundstation-models', [ 'map-services' ]);

/**
 * Service that handles the configuration and map handlers/objects for all the
 * GroundStations.
 */
angular.module('groundstation-models').service('gs', [
    '$log', 'maps', function ($log, maps) {

        'use strict';

        /**
         * Configuration structure for all the GroundStations.
         * @type { { id: { marker: m, cfg: data } } }
         * @private
         */
        this.gsCfg = {};

        /**
         * Creates a new entrance in the configuration structure.
         * @param   {String} gsId Identifier of the new GroundStation.
         * @param   {Object} gsCfg Configuration object for the new GroundStation.
         * @returns {Object} Returns an object with the marker and the configuration.
         */
        this.create = function (gsId, gsCfg) {
            var ll = L.latLng(
                gsCfg.groundstation_latlon[0],
                gsCfg.groundstation_latlon[1]
            ),
                icon = L.icon({
                    iconUrl: '/static/images/icons/gs-icon.svg',
                    iconSize: [30, 30]
                }),
                m = L.marker(
                    ll,
                    { draggable: false, icon: icon }
                ).bindLabel(gsId, { noHide: true });
            return { marker: m, cfg: gsCfg };
        };

        /**
         * Creates a new configuration object for the GroundStation based on the
         * information contained in the data structure.
         * @param data Information as retrieved through JSON-RPC from the server.
         * @returns {*} Leaflet.marker for this GroundStation.
         */
        this.create = function (data) {
            var gsId = data.groundstation_id,
                gsCfg = this.create(gsId, data);
            this.gsCfg[gsId] = gsCfg;
            return maps.getMainMap().then(function (mapInfo) {
                gsCfg.marker.addTo(mapInfo.map);
                return gsCfg;
            });
        };

        /**
         * Removes a given GroundStation from the system, erasing its information
         * from the configuration structure and all related markers.
         * @param gsId The identifier of the GroundStation to be removed.
         */
        this.remove = function (gsId) {
            if (this.gsCfg.hasOwnProperty(gsId) === false) {
                $log.warn('[markers] No marker for gs, id= ' + gsId);
                return;
            }
            this.removeMarker(this.gsCfg[gsId]).then(function () {
                console.log('[gs-model] Marker layer removed, id = ' + gsId);
            });
            delete this.gsCfg[gsId];
            console.log('[gs-model] GS removed, id = ' + gsId);
        };

        /**
         * Removes the marker from the main map.
         * @param   {Leaflet.Marker} marker Marker to be removed.
         * @returns {$q} Promise that returns nothing.
         */
        this.removeMarker = function (marker) {
            return maps.getMap().then(function (map) {
                map.removeLayer(marker);
            });
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
                ll = null,
                newLat = data.groundstation_latlon[0],
                newLng = data.groundstation_latlon[1],
                oldLat = this.gsCfg[gsId].cfg.groundstation_latlon[0],
                oldLng = this.gsCfg[gsId].cfg.groundstation_latlon[1];
            if (newLat !== oldLat) {
                llChanged = true;
            }
            if (newLng !== oldLng) {
                llChanged = true;
            }
            if (llChanged === true) {
                ll = L.latLng(newLat, newLng);
                this.gsCfg[gsId].cfg.groundstation_latlon[0] = newLat;
                this.gsCfg[gsId].cfg.groundstation_latlon[1] = newLng;
                this.gsCfg[gsId].marker.setLatLng(ll);
            }
        };

        /**
         * Updates the configuration of a given GroundStation with the information
         * contained in the data parameter.
         * @param data Data structure as gathered from the JSON-RPC server.
         */
        this.configure = function (data) {
            var gsId = data.groundstation_id;
            console.log('@configure(' + gsId + ')');
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
         * @param {Object} data holding the configuration for the GroundStations.
         * @returns {String} Human-readable string.
         */
        this.asString = function (data) {
            var gs =  null, gsBuffer = '', buffer = '', i;
            for (i = 0; i < data.length; i += 1) {
                gs = data[i];
                gsBuffer = '"id": ' + gs.cfg.groundstation_id + ', ' +
                        '"cfg": ' + JSON.stringify(gs.cfg);
                buffer += gsBuffer;
            }
            return buffer;
        };

    }]);