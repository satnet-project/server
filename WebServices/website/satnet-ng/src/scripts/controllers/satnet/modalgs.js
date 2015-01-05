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
        'ui.bootstrap',
        'nya.bootstrap.select',
        'leaflet-directive',
        'satnet-services',
        'map-services',
        'broadcaster'
    ]
);

angular.module('ui-modalgs-controllers')
    .constant('GS_ELEVATION', 15.0)
    .controller('AddGSModalCtrl', [
        '$scope',
        '$log',
        '$modalInstance',
        'satnetRPC',
        'maps',
        'broadcaster',
        'GS_ELEVATION',
        function (
            $scope,
            $log,
            $modalInstance,
            satnetRPC,
            maps,
            broadcaster,
            GS_ELEVATION
        ) {

            'use strict';

            $scope.gs = { identifier: '', callsign: '', elevation: GS_ELEVATION };

            angular.extend($scope, {
                center: {},
                markers: {},
                layers: { baselayers: {}, overlays: {} }
            });

            maps.autocenterMap($scope, 8).then(function () {
                $log.info('[map-ctrl] GS Modal dialog loaded.');
            });

            $scope.ok = function () {
                var newGsCfg = [
                    $scope.gs.identifier,
                    $scope.gs.callsign,
                    $scope.gs.elevation.toFixed(2),
                    $scope.markers.gs.lat.toFixed(6),
                    $scope.markers.gs.lng.toFixed(6)
                ];
                satnetRPC.rCall('gs.add', newGsCfg).then(function (data) {
                    var gsId = data.groundstation_id;
                    $log.info('[map-ctrl] GS added, id = ' + gsId);
                    broadcaster.gsAdded(gsId);
                    $modalInstance.close();
                });
            };

            $scope.cancel = function () { $modalInstance.close(); };

        }
    ]);

angular.module('ui-modalgs-controllers')
    .constant('GS_ELEVATION', 15.0)
    .controller('EditGSModalCtrl', [
        '$scope', '$log', '$modalInstance', 'satnetRPC', 'broadcaster', 'maps', 'groundstationId',
        function ($scope, $log, $modalInstance, satnetRPC, broadcaster, maps, groundstationId) {
            'use strict';

            $scope.gs = { identifier: '', callsign: '', elevation: 0 };

            angular.extend($scope, {
                center: {},
                markers: {},
                layers: { baselayers: {}, overlays: {} }
            });

            maps.centerAtGs($scope, groundstationId, 8).then(function (gs) {
                $scope.gs.identifier = gs.groundstation_id;
                $scope.gs.callsign = gs.groundstation_callsign;
                $scope.gs.elevation = gs.groundstation_elevation;
                $log.info('[map-ctrl] GS Modal dialog loaded.');
            });

            $scope.update = function () {
                var newGsCfg = {
                    'groundstation_id': groundstationId,
                    'groundstation_callsign': $scope.gs.callsign,
                    'groundstation_elevation': $scope.gs.elevation.toFixed(2),
                    'groundstation_latlon': [
                        $scope.markers.gs.lat.toFixed(6),
                        $scope.markers.gs.lng.toFixed(6)
                    ]
                };
                satnetRPC.rCall('gs.update', [groundstationId, newGsCfg])
                    .then(function (data) {
                        $log.info('[map-ctrl] GS updated, id = ' + data);
                        broadcaster.gsUpdated(groundstationId);
                        $modalInstance.close();
                    });
            };

            $scope.cancel = function () { $modalInstance.close(); };

            $scope.erase = function () {
                if (confirm('Delete this ground station?') === true) {
                    satnetRPC.rCall('gs.delete', [groundstationId]).then(
                        function (gsId) {
                            $log.info('[modalgs] GS removed, id = ' + JSON.stringify(gsId));
                            broadcaster.gsRemoved(gsId);
                            $modalInstance.close();
                        }
                    );
                }
            };

        }
    ]);