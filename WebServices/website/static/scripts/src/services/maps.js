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
 * Created by rtubio on 11/01/14.
 */

/** Module definition (empty array is vital!). */
angular.module('map-services', [ 'leaflet-directive', 'common' ]);

angular.module('map-services')
    .constant('_T_OPACITY', 0.125)
    .constant('_ZOOM', 7)
    .constant('_DETAIL_ZOOM', 10)
    .constant('_DEFAULT_MOVEME', 'Drag me!')
    .service('maps', [
        '$q', '$http', 'common', 'leafletData',
        '_ZOOM', '_DETAIL_ZOOM', '_T_OPACITY', '_DEFAULT_MOVEME',
        function (
            $q, $http, common, leafletData,
            _ZOOM, _DETAIL_ZOOM, _T_OPACITY, _DEFAULT_MOVEME
        )
{
    
    'use strict';
    
    /**
     * Returns the mapInfo structure for the rest of the chained
     * promises.
     * @returns {$q} Promise that returns the mapInfo structure with
     *               a reference to the Leaflet map object.
     */
    this.getMainMap = function () {
        return leafletData.getMap().then(function (map) {
            return { map: map };
        });
    };
    
    /**
     * Creates the main map and adds a terminator for the illuminated
     * surface of the Earth.
     * @param   {boolean} terminator [[Description]]
     * @returns {$q} Promise that returns the mapInfo object
     *               {map, terminator}.
     */
    this.createTerminatorMap = function (terminator) {
        return this.getMainMap().then(function (mapInfo) {
            var t = null;
            if ( terminator ) {
                t = L.terminator({ fillOpacity: _T_OPACITY });
                t.addTo(mapInfo.map);
            }
            mapInfo.terminator = t;
            return mapInfo;
        });
    };

    /**
     * This promise returns a simple object with a reference to the
     * just created map.
     * @param terminator If 'true' adds the overlaying terminator line.
     * @returns {$q} Promise that returns the 'mapData' structure with
     *               a reference to the Leaflet map and to the
     *               terminator overlaying line (if requested).
     */
    this.createMainMap = function (terminator) {
        
        var p = [
            this.createTerminatorMap(terminator),
            common.getUserLocation()
        ];
        
        return $q.all(p).then(function(results) {
            var ll = new L.LatLng(results[1].lat, results[1].lng);
            results[0].map.setView(ll, _ZOOM);
            return({
                map: results[0].map,
                terminator: results[0].terminator,
                center: {
                    lat: results[1].lat, lng: results[1].lng
                }
            });
        });
        
    };
        
    /**
     * Initializes the map, centers it with the estimated position
     * of the user (GeoIP) and adds a "move-me" draggable marker.
     * @param {L} map Reference to the Leaflet map.
     * @param {String} message Message to be added to the marker.
     * @returns {$q} Promise that returns the 'mapData' structure with
     *               an additional marker.
     */
    this.createMoveMeMap = function(map, message) {

        if ( message === null ) { message = _DEFAULT_MOVEME; }
        
        return common.getUserLocation().then(function (location) {
            var lat = location.lat, lng = location.lng;
            var ll = new L.LatLng(lat, lng);
            var marker = L.marker({
                lat: lat, lng: lng,
                message: message, focus: true, draggable: true
            });

            map.setView(ll, _DETAIL_ZOOM);
            marker.addTo(map);
            
            return({
                map: map, marker: marker, center: {
                    lat: location.lat, lng: location.lng
                }
            });

        });
        
    };

    /**
     * Returns a string with the data from a MapInfo like structure.
     * @param   {Object} mapInfo The structure to be printed out.
     * @returns {String} Human-readable representation (string).
     */
    this.asString = function(mapInfo) {
        return 'mapInfo = {' + 
                '"center": ' + JSON.stringify(mapInfo.center) + ', ' +
                '"terminator": ' + mapInfo.terminator + ', ' +
                '"map": ' + mapInfo.map +
            '}';
    };
    
}]);