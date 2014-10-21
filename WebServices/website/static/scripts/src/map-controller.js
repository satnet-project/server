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
var USER_ZOOM = 8;
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
        if ( marker != null ) {
            marker.lat = DEFAULT_LAT; marker.lng = DEFAULT_LNG;
        }

    });

}

////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////// Main Application Module
////////////////////////////////////////////////////////////////////////////////

// This is the main controller for the map.
var app = angular.module('satellite.tracker.js', [
    'leaflet-directive', 'ngResource', 'ui.bootstrap', 'remoteValidation',
    'ngCookies', 'jsonrpc'
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
                    $delegate.warn.apply(null, ['[warn] ' + arguments[0]]);
                    rScope.$broadcast('warnEvent', arguments[0]);
                }
            }
        });
    });

    app.service('satnetRPC', function(jsonrpc, $location) {
        var rpc_path = ''
            + $location.protocol() + "://"
            + $location.host() + ':' + $location.port()
            + '/jrpc/';
        var cfg_service = jsonrpc.newService('configuration', rpc_path);
        // Configuration methods (Ground Stations)
        this.listGS = cfg_service.createMethod('gs.list');
        this.addGS = cfg_service.createMethod('gs.create');
        this.getGSCfg = cfg_service.createMethod('gs.getConfiguration');
        this.setGSCfg = cfg_service.createMethod('gs.setConfiguration');
        this.deleteGS = cfg_service.createMethod('gs.delete');
        // Configuration methods (Spacecraft)
        this.listSC = cfg_service.createMethod('sc.list');
        this.listSC = cfg_service.createMethod('sc.create');
    });

    app.run(function($rootScope, $log, $http, $cookies){
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
        function($scope, $log) {}
    ]);

    app.controller('SCAreaController', ['$scope', '$log',
        function($scope, $log) {}
    ]);

    app.controller('MapController', [
        '$scope', '$log', '$resource', 'leafletData',
        function($scope, $log, $resource, leafletData) {
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
        '$scope', '$log', '$modal', 'satnetRPC',
        function($scope, $log, $modal, satnetRPC) {
            $scope.gsIds = [];
            $scope.addGroundStation = function() {
                var modalInstance = $modal.open({
                    templateUrl: '/static/scripts/src/templates/addGroundStation.html',
                    controller: 'AddGSModalCtrl',
                    backdrop: 'static'
                });
            };
            $scope.editGroundStation = function(g) {
                var modalInstance = $modal.open({
                    templateUrl: '/static/scripts/src/templates/editGroundStation.html',
                    controller: 'EditGSModalCtrl',
                    backdrop: 'static',
                    resolve: {
                        groundstationId: function() { return(g); }
                    }
                });
            };
            $scope.refreshGSList = function() {
                var rpc_call = satnetRPC.listGS().success(function(data) {
                    $log.info('[satnet-jrpc] GroundStations found = '
                        + JSON.stringify(data));
                    $scope.gsIds = data.slice(0);
                });
                rpc_call.error(function(error) {
                    $log.error('[satnet-jrpc] Error calling \"listGS()\" = '
                        + JSON.stringify(error));
                });
            };
            $scope.refreshGSList();
        }
    ]);

    app.controller('SCMenuController', [
        '$scope', '$log', '$modal', 'satnetRPC',
        function($scope, $log, $modal, satnetRPC) {
            $scope.scIds = [];
            $scope.addSpacecraft = function() {
                var modalInstance = $modal.open({
                    templateUrl: '/static/scripts/src/templates/addSpacecraft.html',
                    controller: 'AddSCModalCtrl',
                    backdrop: 'static'
                });
            };
            /*
            $scope.editSpacecraft = function(g) {
                var modalInstance = $modal.open({
                    templateUrl: '/static/scripts/src/templates/editGroundStation.html',
                    controller: 'EditGSModalCtrl',
                    backdrop: 'static',
                    resolve: {
                        groundstationId: function() { return(g); }
                    }
                });
            };
            */
            $scope.refreshSCList = function() {
                var rpc_call = satnetRPC.listSC().success(function(data) {
                    $log.info('[satnet-jrpc] Spacecraft found = '
                        + JSON.stringify(data));
                    $scope.scIds = data.slice(0);
                });
                rpc_call.error(function(error) {
                    $log.error('[satnet-jrpc] Error calling \"listGS()\" = '
                        + JSON.stringify(error));
                });
            };
            $scope.refreshSCList();
        }
    ]);

    app.controller('ExitMenuCtrl', [
        '$scope', '$log', function($scope, $log) {
            $scope.home = function () { $log.info('Exiting...'); };
        }
    ]);

    app.controller('AddGSModalCtrl', [
        '$scope', '$log', '$modalInstance', 'leafletData', 'satnetRPC',
        function ($scope, $log, $modalInstance, leafletData, satnetRPC) {
            $scope.gs = {};
            $scope.gs.identifier = '';
            $scope.gs.callsign = '';
            $scope.gs.elevation = DEFAULT_GS_ELEVATION;
            angular.extend($scope, {
                center: {
                    lat: DEFAULT_LAT, lng: DEFAULT_LNG, zoom: DEFAULT_ZOOM
                },
                markers: {
                    gsMarker: {
                        lat: DEFAULT_LAT, lng: DEFAULT_LNG,
                        message: "Move me!", focus: true, draggable: true
                    }
                }
            });
            leafletData.getMap().then(function(map) {
                locateUser($log, map, $scope.markers.gsMarker);
            });
            $scope.ok = function () {
                var new_gs_cfg = [
                    $scope.gs.identifier,
                    $scope.gs.callsign,
                    $scope.gs.elevation.toFixed(2),
                    $scope.markers.gsMarker.lat.toFixed(6),
                    $scope.markers.gsMarker.lng.toFixed(6)
                ];
                satnetRPC.addGS(new_gs_cfg).success(function (data) {
                    $log.info('[map-ctrl] GS successfully added, id = '
                        + data['groundstation_id']
                    );
                }).error(function (error) {
                    $log.error('[map-ctrl] Could not add GS, reason = '
                        + JSON.stringify(error)
                    );
                });

                $modalInstance.close();
            };
            $scope.cancel = function () { $modalInstance.close(); };
        }
    ]);

    app.controller('EditGSModalCtrl', [
        '$scope', '$log', '$modalInstance', 'leafletData', 'satnetRPC',
        'groundstationId',
        function (
            $scope, $log, $modalInstance, leafletData, satnetRPC,
            groundstationId
        ) {
            $scope.gs = {};
            $scope.center = {
                lat: DEFAULT_LAT, lng: DEFAULT_LNG, zoom: DEFAULT_ZOOM
            };
            $scope.markers = {};
            satnetRPC.getGSCfg([groundstationId]).success(function(data) {
                $log.info(
                    '[map-ctrl] GS configuration retrieved: '
                        + JSON.stringify(data)
                );
                $scope.gs.identifier = groundstationId;
                $scope.gs.callsign = data['groundstation_callsign'];
                $scope.gs.elevation = data['groundstation_elevation'];
                angular.extend($scope, {
                    center: {
                        lat: data['groundstation_latlon'][0],
                        lng: data['groundstation_latlon'][1],
                        zoom: DEFAULT_ZOOM
                    },
                    markers: {
                        gsMarker: {
                            lat: data['groundstation_latlon'][0],
                            lng: data['groundstation_latlon'][1],
                            message: "Move me!", focus: true, draggable: true
                        }
                    }
                });
            }).error(function (error) {
                $log.error(
                    '[map-ctrl] Could not load configuration for GS'
                        + ', id = ' + groundstationId + ', error = '
                        + JSON.stringify(error)
                );
            });
            $scope.update = function () {
                var new_gs_cfg = {
                    'groundstation_id': $scope.gs.identifier,
                    'groundstation_callsign': $scope.gs.callsign,
                    'groundstation_elevation': $scope.gs.elevation.toFixed(2),
                    'groundstation_latlon': [
                        $scope.markers.gsMarker.lat.toFixed(6),
                        $scope.markers.gsMarker.lng.toFixed(6)
                    ]
                };
                satnetRPC.setGSCfg([$scope.gs.identifier, new_gs_cfg]).success(function (data) {
                    $log.info('[map-ctrl] GS successfully configured, id = '
                        + data['groundstation_id']
                    );
                }).error(function (error) {
                    $log.error(
                        '[map-ctrl] Could not set configuration for GS'
                            + ', id = ' + groundstationId + ', error = '
                            + JSON.stringify(error)
                    );
                });
                $modalInstance.close();
            };
            $scope.cancel = function () { $modalInstance.close(); };
            $scope.erase = function () {
                if ( confirm('Delete this ground station?') == true ) {
                    satnetRPC.deleteGS([groundstationId]);
                    $log.info(
                        '[map-ctrl] Ground station removed, id = '
                            + groundstationId
                    );
                    $modalInstance.close();
                }
            };
        }
    ]);

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////// SPACECRAFT MODAL DIALOGS
////////////////////////////////////////////////////////////////////////////////

    app.controller('AddSCModalCtrl', [
        '$scope', '$log', '$modalInstance', 'satnetRPC',
        function ($scope, $log, $modalInstance, satnetRPC) {
            $scope.sc = {};
            $scope.sc.identifier = '';
            $scope.sc.callsign = '';
            $scope.sc.tleid = '';
            $scope.ok = function () {
                var new_sc_cfg = [
                    $scope.sc.identifier,
                    $scope.sc.callsign,
                    $scope.sc.tleid
                ];
                satnetRPC.addSC(new_sc_cfg).success(function (data) {
                    $log.info('[map-ctrl] SC successfully added, id = '
                        + data['spacecraft_id']
                    );
                }).error(function (error) {
                    $log.error('[map-ctrl] Could not add GS, reason = '
                        + JSON.stringify(error)
                    );
                });
                $modalInstance.close();
            };
            $scope.cancel = function () { $modalInstance.close(); };
        }
    ]);
