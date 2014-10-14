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
var DEFAULT_ZOOM = 6;
var DEFAULT_GS_ELEVATION = 15.0;
var USER_ZOOM = 6;
//var TIMESTAMP_FORMAT = 'yyyy-MM-dd-HH:mm:ss.sss';
var TIMESTAMP_FORMAT = 'HH:mm:ss.sss';

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
 * @param $log AngularJS logger object.
 * @param map The map where the user position is to be located.
 * @param marker OPTIONAL parameter with a reference to a marker object that is
 *                  suppose to hold current user's position.
 */
function locateUser ($log, map, marker) {

    $.get('http://ipinfo.io', function (data) {

        var ll = data['loc'].split(',');
        var lat = parseFloat(ll[0]);
        var lng = parseFloat(ll[1]);

        $log.info('[map-ctrl] User located at = ' + ll);
        centerMap(map, lat, lng, USER_ZOOM);
        if ( marker != null ) { marker.lat = lat; marker.lng = lng; }

    }, 'jsonp')
    .fail( function() {
        $log.warn('[map-ctrl] Could not locate user');
        centerMap(map, DEFAULT_LAT, DEFAULT_LNG, DEFAULT_ZOOM);
    });

}

////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////// Main Application Module
////////////////////////////////////////////////////////////////////////////////

// This is the main controller for the map.
var app = angular.module('satellite.tracker.js', [
    'leaflet-directive', 'ngResource', 'ui.bootstrap', 'remoteValidation',
    'ngCookies'
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

    app.factory('restGS', function($resource) {
        return $resource('/configuration/groundstations/');
    });

    app.run(function($rootScope, $log, $http, $cookies) {
        $log.setScope($rootScope);
        $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
    });

    app.controller('NotificationAreaController', ['$scope', '$filter',
        function($scope, $filter) {
            $scope.eventLog = [];
            $scope.$on('infoEvent', function(event, message) {
                $scope.eventLog.unshift({
                    'type': event['name'],
                    'timestamp': $filter('date')(new Date(), TIMESTAMP_FORMAT),
                    'msg':  message
                });
            });
        }
    ]);

    app.controller('GSAreaController', ['$scope', '$log',
        function($scope, $log) {
        }
    ]);

    app.controller('SCAreaController', ['$scope', '$log',
        function($scope, $log) {
        }
    ]);

    app.controller('MapController', [
        '$scope', '$log', '$resource', 'leafletData', 'restGS',
        function($scope, $log, $resource, leafletData, restGS) {
            angular.extend($scope, {
                center: {
                    lat: DEFAULT_LAT, lng: DEFAULT_LNG, zoom: DEFAULT_ZOOM
                }
            });
            leafletData.getMap().then(function(map) {
                locateUser($log, map, null);
            });
        }
    ]);

    app.controller('GSMenuController', [
        '$scope', '$log', '$modal',
        function($scope, $log, $modal) {
            $log.info('[map-ctrl] Adding GS modal...');
            $scope.addGroundStation = function() {
                var modalInstance = $modal.open({
                    templateUrl: '/static/scripts/src/templates/addGroundStation.html',
                    controller: 'AddGSModalCtrl',
                    backdrop: 'static'
                });
            }
        }
    ]);

    app.controller('AddGSModalCtrl', [
        '$scope', '$log', '$modalInstance', 'leafletData', 'restGS',
        function($scope, $log, $modalInstance, leafletData, restGS) {
            $scope._rest_gs = restGS;
            // data models
            $scope.gs = {};
            $scope.gs.identifier = '';
            $scope.gs.callsign = '';
            $scope.gs.elevation = DEFAULT_GS_ELEVATION;
            // map initialization
            angular.extend($scope, {
                center: {
                    lat: DEFAULT_LAT, lng: DEFAULT_LNG, zoom: DEFAULT_ZOOM
                },
                markers: {
                    gsMarker: {
                        lat: DEFAULT_LAT,
                        lng: DEFAULT_LNG,
                        message: "Move me!",
                        focus: true,
                        draggable: true
                    }
                }
            });
            leafletData.getMap().then(function(map) {
                locateUser($log, map, $scope.markers.gsMarker);
            });
            // modal buttons
            $scope.ok = function () {
                var new_gs_cfg = {
                    'identifier'    : $scope.gs.identifier,
                    'callsign'      : $scope.gs.callsign,
                    'elevation'     : $scope.gs.elevation,
                    'latitude'      : $scope.markers.gsMarker.lat,
                    'longitude'     : $scope.markers.gsMarker.lng
                };
                $log.info('[map-ctrl] New GS, cfg = '
                    + JSON.stringify(new_gs_cfg));

                $scope._rest_gs.save(new_gs_cfg);
                //var new_gs = new resource_gs(new_gs_cfg);
                //new_gs.$save();

                $modalInstance.close();
            };
            $scope.cancel = function () {
                $log.info('[map-ctrl] Canceling...');
                $modalInstance.close();
            };
        }
    ]);