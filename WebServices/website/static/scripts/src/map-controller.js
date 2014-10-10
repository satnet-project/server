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
var TIMESTAMP_FORMAT = 'yyyy-MM-dd-HH:mm:ss.sss';

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
    $.get('http://ipinfo.io',
        function (data) {
            var ll = data['loc'].split(',');
            $log.info('[map-controller] User located at = ' + ll);
            centerMap(map, ll[0], ll[1], USER_ZOOM);
        }, 'jsonp')
    .fail(
        function() {
            $log.warn('[map-controller] Could not locate user');
            centerMap(map, DEFAULT_LAT, DEFAULT_LNG, DEFAULT_ZOOM);
        }
    );
}

// This is the main controller for the map.
var app = angular.module('satellite.tracker.js', [
    'leaflet-directive', 'ngResource', 'ui.bootstrap'
]);

    app.config(function($provide) {
        $provide.decorator('$log', function($delegate) {
            var rScope = null;
            return  {
                setScope: function(scope) {
                    rScope = scope;
                },
                log: function () {
                    $delegate.log.apply(null, ['[log] ' + arguments[0]]);
                    rScope.$broadcast('logEvent', arguments[0]);
                },
                info: function () {
                    $delegate.info.apply(null, ['[info] ' + arguments[0]]);
                    rScope.$broadcast('infoEvent', arguments[0]);
                },
                error: function () {
                    $delegate.error.apply(null, ['[error] ' + arguments[0]]);
                    rScope.$broadcast('errEvent', arguments[0]);
                },
                warn: function () {
                    $delegate.info.apply(null, ['[warn] ' + arguments[0]]);
                    rScope.$broadcast('warnEvent', arguments[0]);
                }
            }
        });
    });
    app.factory('listGroundStations', function($resource) {
        return $resource('/configuration/groundstations', {});
    });

    app.run(function($rootScope, $log) { $log.setScope($rootScope); })
    app.controller('NotificationAreaController', ['$scope', '$filter',
        function($scope, $filter) {
            $scope.eventLog = [];
            $scope.$on('infoEvent', function(event, message) {
                $scope.eventLog.push({
                    'type': event['name'],
                    'timestamp': $filter('date')(new Date(), TIMESTAMP_FORMAT),
                    'msg':  message
                });
            });
        }
    ]);

    app.controller('GSAreaController', ['$scope', '$log',
        function($scope, $log) {
            // Include here the listeners to the broadcasted log messages.
        }
    ]);

    app.controller('SCAreaController', ['$scope', '$log',
        function($scope, $log) {
            // Include here the listeners to the broadcasted log messages.
        }
    ]);

    app.controller('MapController', [
        '$scope', '$log', '$resource', 'leafletData', 'listGroundStations',
        function($scope, $log, $resource, leafletData, listGroundStations) {
            angular.extend($scope, {
                center: {
                    lat: DEFAULT_LAT, lng: DEFAULT_LNG, zoom: DEFAULT_ZOOM
                }
            });
            leafletData.getMap().then(function(map) {
                locateUser($log, map);
            });
            $scope.init = function() {
                $scope._simulator = new Simulator($log, listGroundStations);
            };
        }
    ]);