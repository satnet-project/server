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

/**
 * This function centers the map at the given [lat, long] coordinates
 * with the specified zoom level.
 * @param $scope
 * @param lat Latitude (coordinates).
 * @param lng Longitude (coordinates).
 * @param zoom Level of zoom.
 */
function centerMap ($scope, lat, lng, zoom) {
    angular.extend($scope, { center: { lat: lat, lng: lng, zoom: zoom } });
}

/**
 * This function locates the map at the location of the IP that the
 * client uses for this connection.
 */
function locateUser ($scope, $log) {
    $.get("http://ipinfo.io",
        function (data) {
            var ll = data['loc'].split(',');
            $log.info('User located at = ' + ll);
            centerMap($scope, ll[0], ll[1], MapController._DEFAULT_ZOOM);
        }, 'jsonp')
    .fail(
        function(data) {
            $log.warn('Could not locate user');
            centerMap($scope,
                MapController._DEFAULT_LAT, MapController._DEFAULT_LON,
                MapController._DEFAULT_ZOOM
            );
        }
    );
}

/**
 * Constructor for the MapController object.
 * @param $scope
 * @param $log
 * @constructor
 */
function MapController($scope, $log) {
    this._DEFAULT_LAT = 42.6000;
    this._DEFAULT_LON = -8.9330;
    this._DEFAULT_ZOOM = 10;
    locateUser($scope, $log);
}

var app = angular
    .module("satellite.tracker.js", ['leaflet-directive'])
    .controller("MapController", MapController);