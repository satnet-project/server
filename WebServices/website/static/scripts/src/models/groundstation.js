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
angular.module('groundstation-models', [ 'satnet-services' ]);

/**
 * Service that handles the configuration and map handlers/objects for all the
 * GroundStations.
 */
angular.module('groundstation-models').service('gs', [
    '$rootScope', '$log', function($rootScope, $log) {
        
    'use strict';

    /**
     * Configuration structure for all the GroundStations.
     * @type { { id: { marker: m, cfg: data } } }
     * @private
     */
    this._gsCfg = {};

    /**
     * Creates a new configuration object for the GroundStation based on the
     * information contained in the data structure.
     * @param data Information as retrieved through JSON-RPC from the server.
     * @returns {*} Leaflet.marker for this GroundStation.
     */
    this.create = function(data) {
        var gsId = data['groundstation_id'];
        if ( gsId in this._gsCfg ) {
            $log.warn('[markers] Marker exists, id = ' + gsId);
        }
        var ll = L.latLng(
            data['groundstation_latlon'][0],
            data['groundstation_latlon'][1]
        );
        var icon = L.icon({
            iconUrl: '/static/images/icons/gs-icon.svg',
            iconSize: [30, 30]
            });
        var m = L.marker(
            ll, { draggable: false, icon: icon }
        ).bindLabel(gsId, { noHide: true });
        this._gsCfg[gsId] = { marker: m, cfg: data };
        return m;
    };

    /**
     * Removes a given GroundStation from the system, erasing its information
     * from the configuration structure and all related markers.
     * @param gsId The identifier of the GroundStation to be removed.
     */
    this.remove = function(gsId) {
        if ( ( gsId in this._gsCfg ) === false ) {
            $log.warn('[markers] No marker for gs, id= ' + gsId);
            return;
        }
        $rootScope._map.removeLayer(this._gsCfg[gsId].marker);
        delete this._gsCfg[gsId];
    };

    /**
     * Dirty check and update of the position of the GroundStation (both in
     * the configuration structure and in its marker).
     * @param gsId The identifier of the GroundStation.
     * @param data The new configuration for the GroundStation.
     * @private
     */
    this._latlngDirtyUpdate = function (gsId, data) {
        var llChanged = false;
        var newLat = data['groundstation_latlon'][0];
        var newLng = data['groundstation_latlon'][1];
        var oldLat = this._gsCfg[gsId].cfg['groundstation_latlon'][0];
        var oldLng = this._gsCfg[gsId].cfg['groundstation_latlon'][1];
        if ( newLat !== oldLat ) { llChanged = true; }
        if ( newLng !== oldLng ) { llChanged = true; }
        if ( llChanged === true ) {
            var ll = L.latLng(newLat, newLng);
            this._gsCfg[gsId].cfg['groundstation_latlon'][0] = newLat;
            this._gsCfg[gsId].cfg['groundstation_latlon'][1] = newLng;
            this._gsCfg[gsId].marker.setLatLng(ll);
        }
    };

    /**
     * Updates the configuration of a given GroundStation with the information
     * contained in the data parameter.
     * @param data Data structure as gathered from the JSON-RPC server.
     */
    this.configure = function(data) {
        var gsId = data['groundstation_id'];
        if ( ! gsId in this._gsCfg ) {
            $log.warn('[markers] No marker for gs, id= ' + gsId);
            return;
        }
        // Callsign and minimum contact elevation are directly updated.
        this._gsCfg[gsId].cfg['groundstation_callsign']
            = data['groundstation_callsign'];
        this._gsCfg[gsId].cfg['groundstation_elevation']
            = data['groundstation_elevation'];
        // LAT/LNG dirty check + update only if necessary. This way,
        // unnecessary marker's redrawings are avoided.
        this._latlngDirtyUpdate(gsId, data);
    };

}]);