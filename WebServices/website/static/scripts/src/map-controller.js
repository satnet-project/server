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

// DEFAULT values for the applications
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
    'leaflet-directive',
    'ui.bootstrap', 'nya.bootstrap.select',
    'ngResource', 'ngCookies',
    'remoteValidation', 'jsonrpc'
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

    app.service('celestrak', function($http) {
        this.readTLE = function (subsection, successCb) {
            var uri = __CELESTRAK_RESOURCES[subsection];
            var corss_uri = getCORSSURL(uri);
            return $http.get(corss_uri).success(function (data) {
                successCb(readTLEs(data));
            }).error(function (data) {
                throw '[celestrak] Error = ' + JSON.stringify(data);
            });
        };
    });

    app.service('satnetRPC', function(jsonrpc, $location, $log) {
        var rpc_path = ''
            + $location.protocol() + "://"
            + $location.host() + ':' + $location.port()
            + '/jrpc/';
        this._cfg_service = jsonrpc.newService('configuration', rpc_path);
        this._services = {
            // Configuration methods (Ground Stations)
            'gs.list': this._cfg_service.createMethod('gs.list'),
            'gs.add': this._cfg_service.createMethod('gs.create'),
            'gs.get': this._cfg_service.createMethod('gs.getConfiguration'),
            'gs.update': this._cfg_service.createMethod('gs.setConfiguration'),
            'gs.delete': this._cfg_service.createMethod('gs.delete'),
            // Configuration methods (Spacecraft)
            'sc.list': this._cfg_service.createMethod('sc.list'),
            'sc.add': this._cfg_service.createMethod('sc.create'),
            'sc.get': this._cfg_service.createMethod('sc.getConfiguration'),
            'sc.update': this._cfg_service.createMethod('sc.setConfiguration'),
            'sc.delete': this._cfg_service.createMethod('sc.delete')
        };
        this._errorCb = function(data) {
            $log.warn(
                '[satnet-jrpc] Error calling \"satnetRPC\" = '
                    + JSON.stringify(data)
            );
        };
        this.call = function (service, paramArray, successCb, errorCb) {
            if ( ! service in this._services ) {
                throw '\"satnetRPC\" service not found, id = ' + service;
            }
            if ( errorCb == null ) { errorCb = this._errorCb; }
            this._services[service](paramArray)
                .success(successCb).error(errorCb);
        };
    });

    app.service('gs', function($rootScope, $log) {
        this._gsCfg = {};
        this.create = function(data) {
            var gs_id = data['groundstation_id'];
            var ll = L.latLng(
                data['groundstation_latlon'][0],
                data['groundstation_latlon'][1]
            );
            var icon = L.icon({
                iconUrl: '/static/images/icons/gs-icon.svg',
                iconSize: [30, 30]
            });
            var caption = gs_id + '@' + data['groundstation_callsign'];
            var m = L.marker(ll, { draggable: false, icon: icon })
                                .bindLabel(caption, { noHide: true });
            this._gsCfg[gs_id] = { marker: m, cfg: data };
            return m;
        };
        this.remove = function(gs_id) {
            if ( ! gs_id in this._gsCfg ) {
                $log.warn('[markers] No marker for gs, id= ' + gs_id);
                return;
            }
            $rootScope._map.removeLayer(this._gsCfg[gs_id]['marker']);
            delete this._gsCfg[gs_id];
        };
        this.configure = function(data) {
            var gs_id = data['groundstation_id'];
            if ( ! gs_id in this._gsCfg ) {
                $log.warn('[markers] No marker for gs, id= ' + gs_id);
                return;
            }
            $log.info('gs_id = ' + gs_id);
            // CALLSIGN DIRTY CHECKING...
            var old_cs = this._gsCfg[gs_id].cfg['groundstation_callsign'];
            var new_cs = data['groundstation_callsign'];
            if ( new_cs != old_cs ) {
                this.remove(gs_id);
                this.create(data);
            }
            else {
                // POSITION DIRTY CHECKING...
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
            }
        };
    });

    app.service('xSatnetRPC', function($rootScope, satnetRPC, gs) {
        this.addGSMarker = function(gs_id) {
            satnetRPC.call('gs.get', [gs_id], function(data) {
                gs.create(data).addTo($rootScope._map);
            });
        };
        this.initGSMarkers = function() {
            satnetRPC.call('gs.list', [], function(data) {
                for ( var i = 0; i < data.length; i++ ) {
                    satnetRPC.call('gs.get', [data[i]], function(data) {
                        gs.create(data).addTo($rootScope._map);
                    });
                }
            });
        };
        this.updateGSMarker = function(gs_id) {
            satnetRPC.call('gs.get', [gs_id], function(data) {
                gs.configure(data);
            });
        };
    });

    app.service('broadcaster', function($rootScope) {
        this.__GS_ADDED_EVENT = 'gs.added';
        this.__GS_REMOVED_EVENT = 'gs.removed';
        this.__GS_UPDATED_EVENT = 'gs.updated';
        this.gsAdded = function(gs_id) {
            $rootScope.$broadcast(this.__GS_ADDED_EVENT, gs_id);
        };
        this.gsRemoved = function(gs_id) {
            $rootScope.$broadcast(this.__GS_REMOVED_EVENT, gs_id);
        };
        this.gsUpdated = function(gs_id) {
            $rootScope.$broadcast(this.__GS_UPDATED_EVENT, gs_id);
        };
    });

    app.run(function($rootScope, $log, $http, $cookies, leafletData){
        $log.setScope($rootScope);
        $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
        leafletData.getMap().then(function(map) { $rootScope._map = map; });
    });

    app.controller('NotificationAreaController',
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
    );

    app.controller('MapController',
        function(
            $scope, $log,
            leafletData, xSatnetRPC, broadcaster, gs
        ) {
            $scope.markers = [];
            angular.extend($scope, {
                center: {
                    lat: DEFAULT_LAT, lng: DEFAULT_LNG, zoom: DEFAULT_ZOOM
                },
                defaults: { worldCopyJump: true }
            });
            leafletData.getMap().then(function(map) {
                locateUser($log, map, null);
                L.terminator({ fillOpacity: 0.125 }).addTo(map);
                xSatnetRPC.initGSMarkers();
            });
            $scope.$on(broadcaster.__GS_ADDED_EVENT, function(event, gs_id) {
                xSatnetRPC.addGSMarker(gs_id);
            });
            $scope.$on(broadcaster.__GS_REMOVED_EVENT, function(event, gs_id) {
                gs.remove(gs_id);
            });
            $scope.$on(broadcaster.__GS_UPDATED_EVENT, function(event, gs_id) {
                xSatnetRPC.updateGSMarker(gs_id);
            });
        }
    );

    app.controller('GSMenuCtrl',
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
                    controller: 'EditGSModalCtrl', backdrop: 'static',
                    resolve: { groundstationId: function() { return(g); } }
                });
            };
            $scope.refreshGSList = function() {
                satnetRPC.call('gs.list', [], function(data) {
                    $scope.gsIds = data.slice(0);
                });
            };
            $scope.refreshGSList();
        }
    );

    app.controller('SCMenuCtrl',
        function($scope, $log, $modal, satnetRPC) {
            $scope.scIds = [];
            $scope.addSpacecraft = function() {
                var modalInstance = $modal.open({
                    templateUrl: '/static/scripts/src/templates/addSpacecraft.html',
                    controller: 'AddSCModalCtrl', backdrop: 'static'
                });
            };
            $scope.editSpacecraft = function(s) {
                var modalInstance = $modal.open({
                    templateUrl: '/static/scripts/src/templates/editSpacecraft.html',
                    controller: 'EditSCModalCtrl', backdrop: 'static',
                    resolve: { spacecraftId: function() { return(s); } }
                });
            };
            $scope.refreshSCList = function() {
                satnetRPC.call('sc.list', [], function(data) {
                    $scope.scIds = data.slice(0);
                });
            };
            $scope.refreshSCList();
        }
    );

    app.controller('ExitMenuCtrl',
        function($scope, $log) {
            $scope.home = function () { $log.info('Exiting...'); };
        }
    );

////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////// GROUND STATIONS MODAL DIALOGS
////////////////////////////////////////////////////////////////////////////////

    app.controller('AddGSModalCtrl',
        function (
            $scope, $log, $modalInstance, leafletData, satnetRPC, broadcaster
        ) {
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
                satnetRPC.call('gs.add', new_gs_cfg, function (data) {
                    var gs_id = data['groundstation_id'];
                    $log.info('[map-ctrl] GS added, id = ' + gs_id);
                    broadcaster.gsAdded(gs_id);
                });
                $modalInstance.close();
            };
            $scope.cancel = function () { $modalInstance.close(); };
        }
    );

    app.controller('EditGSModalCtrl',
        function (
            $scope, $log, $modalInstance,
            leafletData, satnetRPC, broadcaster,
            groundstationId
        ) {
            $scope.gs = {};
            $scope.center = {
                lat: DEFAULT_LAT, lng: DEFAULT_LNG, zoom: DEFAULT_ZOOM
            };
            $scope.markers = {};
            satnetRPC.call('gs.get', [groundstationId], function(data) {
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
            });
            $scope.update = function () {
                var new_gs_cfg = {
                    'groundstation_id': groundstationId,
                    'groundstation_callsign': $scope.gs.callsign,
                    'groundstation_elevation': $scope.gs.elevation.toFixed(2),
                    'groundstation_latlon': [
                        $scope.markers.gsMarker.lat.toFixed(6),
                        $scope.markers.gsMarker.lng.toFixed(6)
                    ]
                };
                satnetRPC.call(
                    'gs.update', [groundstationId, new_gs_cfg],
                    function (data) {
                        $log.info('[map-ctrl] GS updated, id = ' + data);
                        broadcaster.gsUpdated(data);
                    }
                );
                $modalInstance.close();
            };
            $scope.cancel = function () { $modalInstance.close(); };
            $scope.erase = function () {
                if ( confirm('Delete this ground station?') == true ) {
                    satnetRPC.call(
                        'gs.delete', [groundstationId],
                        function (data) {
                            $log.info(
                                '[map-ctrl] GS removed, id = ' + data
                            );
                            broadcaster.gsRemoved(data);
                        }
                    );
                    $modalInstance.close();
                }
            };
        }
    );

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////// SPACECRAFT MODAL DIALOGS
////////////////////////////////////////////////////////////////////////////////

    app.controller('AddSCModalCtrl',
        function ($scope, $log, $modalInstance, satnetRPC, celestrak) {
            $scope.sc = {
                identifier: '',
                callsign: '',
                tlegroup: '',
                tleid: ''
            };

            $scope.tlegroups = __CELESTRAK_SELECT_SECTIONS;
            $scope.tles = [];

            $scope.initTles = function(defaultOption) {
                $scope.tles = celestrak.readTLE(
                    value['subsection'], function (data) {
                        $scope.tles = data.slice(0);
                    }
                );
                $scope.sc.tlegroup = defaultOption;
            };
            $scope.groupChanged = function (value) {
                $scope.tles = celestrak.readTLE(
                    value['subsection'], function (data) {
                        $scope.tles = data.slice(0);
                    }
                );
            };
            $scope.ok = function () {
                var new_sc_cfg = [
                    $scope.sc.identifier,
                    $scope.sc.callsign,
                    $scope.sc.tleid['id']
                ];
                satnetRPC.call('sc.add', new_sc_cfg, function (data) {
                    $log.info('[map-ctrl] SC added, id = '
                        + data['spacecraft_id']
                    );
                });
                $modalInstance.close();
            };
            $scope.cancel = function () { $modalInstance.close(); };
        }
    );

    app.controller('EditSCModalCtrl',
        function (
            $scope, $log, $modalInstance, satnetRPC, celestrak, spacecraftId
        ) {

            $scope.sc = {
                identifier: spacecraftId,
                callsign: '',
                tlegroup: '',
                tleid: '',
                saved_tleid: ''
            };

            $scope.tlegroups = __CELESTRAK_SELECT_SECTIONS;
            $scope.tles = [];

            satnetRPC.call('sc.get', [spacecraftId], function(data) {
                $scope.sc.identifier = spacecraftId;
                $scope.sc.callsign = data['spacecraft_callsign'];
                $scope.sc.saved_tleid = data['spacecraft_tle_id'];
            });

            $scope.initTles = function(defaultOption) {
                $scope.tles = celestrak.readTLE(
                    value['subsection'], function (data) {
                        $scope.tles = data.slice(0);
                    }
                );
                $scope.sc.tlegroup = defaultOption;
            };
            $scope.groupChanged = function (value) {
                $scope.tles = celestrak.readTLE(
                    value['subsection'], function (data) {
                        $scope.tles = data.slice(0);
                    }
                );
            };
            $scope.update = function () {
                var new_sc_cfg = {
                    'spacecraft_id': spacecraftId,
                    'spacecraft_callsign': $scope.sc.callsign,
                    'spacecraft_tle_id': $scope.sc.tleid['id']
                };
                satnetRPC.call(
                    'sc.update', [spacecraftId, new_sc_cfg], function (data) {
                        $log.info('[map-ctrl] SC updated, id = ' + data);
                    }
                );
                $modalInstance.close();
            };
            $scope.cancel = function () { $modalInstance.close(); };
            $scope.erase = function () {
                if ( confirm('Delete this spacecraft?') == true ) {
                    satnetRPC.call('sc.delete', [spacecraftId], function(data) {
                        $log.info(
                            '[map-ctrl] Spacecraft removed, id = ' + data
                        );
                    });
                    $modalInstance.close();
                }
            };
        }
    );