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
angular.module(
    'ui-modalgs-controllers',
    [
        'ui.bootstrap', 'nya.bootstrap.select',
        'leaflet-directive',
        'common', 'satnet-services', 'broadcaster'
    ]
);

angular.module('ui-modalgs-controllers')
    .constant('LAT', 32.630)
    .constant('LNG', 8.933)
    .constant('D_ZOOM', 10)
    .constant('GS_ELEVATION', 15.0)
    .controller('AddGSModalCtrl', [
        '$scope', '$log',
        '$modalInstance',
        'common', 'satnetRPC', 'broadcaster',
        'LAT', 'LNG', 'D_ZOOM', 'GS_ELEVATION',
        function ($scope, $log, $modalInstance, common, satnetRPC, broadcaster, LAT, LNG, D_ZOOM, GS_ELEVATION) {

            'use strict';

            $scope.gs = {};
            $scope.gs.identifier = '';
            $scope.gs.callsign = '';
            $scope.gs.elevation = GS_ELEVATION;

            $scope.center = {};
            $scope.markers = [];

            angular.extend($scope, {
                center: {
                    lat: LAT,
                    lng: LNG,
                    zoom: D_ZOOM
                },
                markers: {
                    gsMarker: {
                        lat: LAT,
                        lng: LNG,
                        message: 'Move me!',
                        focus: true,
                        draggable: true
                    }
                }
            });

            $scope.initMap = function () {
                common.getUserLocation().then(function (location) {
                    $scope.center.lat = location.lat;
                    $scope.center.lng = location.lng;
                    $scope.markers.gsMarker.lat = location.lat;
                    $scope.markers.gsMarker.lng = location.lng;
                });
            };

            $scope.initMap();

            $scope.ok = function () {
                var newGsCfg = [
                    $scope.gs.identifier,
                    $scope.gs.callsign,
                    $scope.gs.elevation.toFixed(2),
                    $scope.markers.gsMarker.lat.toFixed(6),
                    $scope.markers.gsMarker.lng.toFixed(6)
                ];
                satnetRPC.rCall('gs.add', newGsCfg).then(function (data) {
                    var gsId = data.groundstation_id;
                    $log.info('[map-ctrl] GS added, id = ' + gsId);
                    broadcaster.gsAdded(gsId);
                    $modalInstance.close();
                });
            };
            $scope.cancel = function () {
                $modalInstance.close();
            };
        }
    ]);

angular.module('ui-modalgs-controllers')
    .constant('LAT', 32.630)
    .constant('LNG', 8.933)
    .constant('D_ZOOM', 10)
    .constant('GS_ELEVATION', 15.0)
    .controller('EditGSModalCtrl', [
        '$scope', '$log', '$modalInstance',
        'satnetRPC', 'broadcaster', 'maps', 'groundstationId',
        'LAT', 'LNG', 'D_ZOOM',
        function ($scope, $log, $modalInstance, satnetRPC, broadcaster, maps, groundstationId, LAT, LNG, D_ZOOM) {
            'use strict';

            $scope.gs = {};
            $scope.center = {};
            $scope.markers = [];

            angular.extend($scope, {
                center: {
                    lat: LAT,
                    lng: LNG,
                    zoom: D_ZOOM
                },
                markers: {
                    gsMarker: {
                        lat: LAT,
                        lng: LNG,
                        message: 'Move me!',
                        focus: true,
                        draggable: true
                    }
                }
            });

            satnetRPC.rCall('gs.get', [groundstationId]).then(function (cfg) {
                $scope.gs.identifier = groundstationId;
                $scope.gs.callsign = cfg.groundstation_callsign;
                $scope.gs.elevation = cfg.groundstation_elevation;
                angular.extend($scope, {
                    center: {
                        lat: cfg.groundstation_latlon[0],
                        lng: cfg.groundstation_latlon[1],
                        zoom: maps.DEFAULT_ZOOM
                    },
                    markers: {
                        gsMarker: {
                            lat: cfg.groundstation_latlon[0],
                            lng: cfg.groundstation_latlon[1],
                            message: 'Move me!',
                            focus: true,
                            draggable: true
                        }
                    }
                });
            });
            $scope.update = function () {
                var newGsCfg = {
                    'groundstation_id': groundstationId,
                    'groundstation_callsign': $scope.gs.callsign,
                    'groundstation_elevation': $scope.gs.elevation.toFixed(2),
                    'groundstation_latlon': [
                        $scope.markers.gsMarker.lat.toFixed(6),
                        $scope.markers.gsMarker.lng.toFixed(6)
                    ]
                };
                satnetRPC.rCall(
                    'gs.update',
                    [groundstationId, newGsCfg]
                ).then(function (data) {
                    $log.info('[map-ctrl] GS updated, id = ' + data);
                    broadcaster.gsUpdated(groundstationId);
                    $modalInstance.close();
                });
            };
            $scope.cancel = function () {
                $modalInstance.close();
            };
            $scope.erase = function () {
                if (confirm('Delete this ground station?') === true) {
                    satnetRPC.rCall(
                        'gs.delete',
                        [groundstationId]
                    ).then(function (gsId) {
                        $log.info('[map-ctrl] GS removed, id = ' + gsId);
                        broadcaster.gsRemoved(gsId);
                        $modalInstance.close();
                    });
                }
            };

        }
    ]);