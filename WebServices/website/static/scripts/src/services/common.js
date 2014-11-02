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
 * Created by rtubio on 10/30/14.
 */

/** Module definition (empty array is vital!). */
angular.module('common', [ 'leaflet-directive' ]);

/**
 * Service used for broadcasting UI events in between controllers.
 */
angular.module('common')
    .constant('_T_OPACITY', 0.125)
    .constant('_ZOOM', 8)
    .service('common', [
        '$q', '$http', 'leafletData', '_ZOOM', '_T_OPACITY',
        function ($q, $http, leafletData, _ZOOM, _T_OPACITY)
{

    'use strict';

    this.createMap = function (terminator) {
        return leafletData.getMap().then(function (map) {
            var t = null;
            if ( terminator ) {
                t = L.terminator({ fillOpacity: _T_OPACITY });
                t.addTo(map);
            }
            return { 'map': map, 'terminator': t };
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
    this.initMap = function (terminator) {
        
        var d = $q.defer();
        var promises = [
            this.createMap(terminator),
            this.getUserLocation()
        ];
        
        $q.all(promises).then(function(results) {
            console.log('>>> results# = ' + results.length);
            if ( results[0].map === null ) { console.log('XXX'); }
            console.log('> r[0].t = ' + results[0].terminator);
            console.log('> r[1] = ' + results[1]);
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
    
    /**
     * Retrieves the user location using an available Internet service.
     * @returns {$q} Promise that returns a { lat, lng } object.
     */
    this.getUserLocation = function() {
        return $http.jsonp('http://ipinfo.io').then( function (data) {
            console.log('data = ' + JSON.stringify(data));
            var ll = data.loc.split(',');
            var lat = parseFloat(ll[0]);
            var lng = parseFloat(ll[1]);
            return { 'lat': lat, 'lng': lng };
        });
    };
    
    // Proxy to get rid of the CORS restrictions.
    this._CORSS_PROXY = 'http://www.corsproxy.com/';
    // Get rid of this part of the URI to use with corsproxy
    this._CORSS_PROXY_HTTP = 'http://';

    /**
     * Returns a URL modified to be used directly with the corsproxy.com service.
     * @param url The URL to be modified.
     * @returns {string} The ready-to-use URL.
     */
    this.getCORSSURL = function (url) {
        var correctedUrl = url.replace(this._CORSS_PROXY_HTTP, '');
        return(this._CORSS_PROXY + correctedUrl);
    };
    
}]);