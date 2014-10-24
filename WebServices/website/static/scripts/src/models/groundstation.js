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
        var gs_id = data['groundstation_id'];
        if ( gs_id in this._gsCfg ) {
            $log.warn('[markers] Marker exists, id = ' + gs_id);
        }
        var ll = L.latLng(
            data['groundstation_latlon'][0], data['groundstation_latlon'][1]
        );
        var icon = L.icon({
            iconUrl: '/static/images/icons/gs-icon.svg',
            iconSize: [30, 30]
            });
        var m = L.marker(
            ll, { draggable: false, icon: icon }
        ).bindLabel(gs_id, { noHide: true });
        this._gsCfg[gs_id] = { marker: m, cfg: data };
        return m;
    };

    /**
     * Removes a given GroundStation from the system, erasing its information
     * from the configuration structure and all related markers.
     * @param gs_id The identifier of the GroundStation to be removed.
     */
    this.remove = function(gs_id) {
        if ( ! gs_id in this._gsCfg ) {
            $log.warn('[markers] No marker for gs, id= ' + gs_id);
            return;
        }
        $rootScope._map.removeLayer(this._gsCfg[gs_id]['marker']);
        delete this._gsCfg[gs_id];
    };

    /**
     * Dirty check and update of the position of the GroundStation (both in
     * the configuration structure and in its marker).
     * @param gs_id The identifier of the GroundStation.
     * @param data The new configuration for the GroundStation.
     * @private
     */
    this._latlngDirtyUpdate = function (gs_id, data) {
        var ll_changed = false;
        var new_lat = data['groundstation_latlon'][0];
        var new_lon = data['groundstation_latlon'][1];
        var old_lat = this._gsCfg[gs_id].cfg['groundstation_latlon'][0];
        var old_lon = this._gsCfg[gs_id].cfg['groundstation_latlon'][1];
        if ( new_lat != old_lat ) { ll_changed = true; }
        if ( new_lon != old_lon ) { ll_changed = true; }
        if ( ll_changed == true ) {
            var ll = L.latLng(new_lat, new_lon);
            this._gsCfg[gs_id].cfg['groundstation_latlon'][0] = new_lat;
            this._gsCfg[gs_id].cfg['groundstation_latlon'][1] = new_lon;
            this._gsCfg[gs_id].marker.setLatLng(ll);
        }
    };

    /**
     * Updates the configuration of a given GroundStation with the information
     * contained in the data parameter.
     * @param data Data structure as gathered from the JSON-RPC server.
     */
    this.configure = function(data) {
        var gs_id = data['groundstation_id'];
        if ( ! gs_id in this._gsCfg ) {
            $log.warn('[markers] No marker for gs, id= ' + gs_id);
            return;
        }
        // Callsign and minimum contact elevation are directly updated.
        this._gsCfg[gs_id].cfg['groundstation_callsign']
            = data['groundstation_callsign'];
        this._gsCfg[gs_id].cfg['groundstation_elevation']
            = data['groundstation_elevation'];
        // LAT/LNG dirty check + update only if necessary. This way,
        // unnecessary marker's redrawings are avoided.
        this._latlngDirtyUpdate(gs_id, data);
    };

}]);
