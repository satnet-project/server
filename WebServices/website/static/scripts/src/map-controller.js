/**
 * Copyright 2014, 2014 Ricardo Tubio-Pardavila
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
 * Created by rtubio on 1/31/14.
 */

var DEFAULT_LAT = 42.6000;    // lat, lon for Pobra (GZ/ES)
var DEFAULT_LNG = -8.9330;
var DEFAULT_ZOOM = 12;
var USER_ZOOM = 6;

/**
 * This function centers the map at the given [lat, long] coordinates
 * with the specified zoom level.
 * @param map Leaflet map.
 * @param lat Latitude (coordinates).
 * @param lng Longitude (coordinates).
 * @param zoom Level of zoom.
 */
function centerMap (map, lat, lng, zoom) {
    map.setView(new L.LatLng(lat, lng), zoom);
}

/**
 * This function locates the map at the location of the IP that the
 * client uses for this connection.
 */
function locateUser ($log, map) {
    $.get("http://ipinfo.io",
        function (data) {
            var ll = data['loc'].split(',');
            $log.info('User located at = ' + ll);
            centerMap(map, ll[0], ll[1], USER_ZOOM);
        }, 'jsonp')
    .fail(
        function() {
            $log.warn('Could not locate user');
            centerMap(map, DEFAULT_LAT, DEFAULT_LNG, DEFAULT_ZOOM);
        }
    );
}

var app = angular
    .module("satellite.tracker.js", ['leaflet-directive'])
    .controller("MapController", [
        "$scope", "$log", "leafletData", function($scope, $log, leafletData) {
            angular.extend($scope, {
                center: {
                    lat: DEFAULT_LAT,
                    lng: DEFAULT_LNG,
                    zoom: DEFAULT_ZOOM
                }
            });
            leafletData.getMap().then(function(map) {
                locateUser($log, map);
            });
        }
    ]);