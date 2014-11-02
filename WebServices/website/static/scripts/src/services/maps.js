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
    .constant('_ZOOM', 8)
    .service('maps', [
        '$q', '$http', 'common', 'leafletData', '_ZOOM', '_T_OPACITY',
        function ($q, $http, common, leafletData, _ZOOM, _T_OPACITY)
{
    
    /**
     * Returns the mapInfo structure for the rest of the chained
     * promises.
     * @returns {$q} Promise that returns the mapInfo structure with
     *               a reference to the Leaflet map object.
     */
    this.getMapInfo = function () {
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
    this.createMap = function (terminator) {
        return this.getMapInfo().then(function (mapInfo) {
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
    this.centerMap = function (terminator) {
        
        var d = $q.defer();
        var promises = [
            this.createMap(terminator),
            common.getUserLocation()
        ];
        
        $q.all(promises).then(function(results) {
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

        return d.promise;
        
    };
    
    /**
     * Initializes the map, centers it with the estimated position
     * of the user (GeoIP) and adds a "move-me" draggable marker.
     * @returns {$q} Promise that returns the 'mapData' structure with
     *               an additional marker.
     */
    this.centerMoveMeMarker = function() {
        return this.centerMap().then(function(data) {
            data.marker = L.marker({
                lat: data.ll[0], lng: data.ll[1],
                message: 'Move me!',
                focus: true, draggable: true
            });
            data.marker.addTo(data.map);
            return data;
        });
    };
}]);