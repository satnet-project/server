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
    'ui-modalgs-controllers', [
        'leaflet-directive', 'ui.bootstrap', 'nya.bootstrap.select',
        'satnet-services', 'broadcaster'
    ]
);

angular.module('ui-modalgs-controllers').controller('AddGSModalCtrl', [
    '$scope', '$log',
    '$modalInstance', 'leafletData',
    'satnetRPC', 'broadcaster',
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
]);

angular.module('ui-modalgs-controllers').controller('EditGSModalCtrl', [
   '$scope', '$log',
    '$modalInstance', 'leafletData',
    'satnetRPC', 'broadcaster', 'groundstationId',
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
            satnetRPC.call('gs.update', [groundstationId, new_gs_cfg],
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
                satnetRPC.call('gs.delete', [groundstationId], function (data) {
                    $log.info('[map-ctrl] GS removed, id = ' + data);
                    broadcaster.gsRemoved(data);
                });
                $modalInstance.close();
            }
        };
    }
]);