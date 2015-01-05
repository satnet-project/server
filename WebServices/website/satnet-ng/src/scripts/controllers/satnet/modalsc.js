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
    'ui-modalsc-controllers',
    [
        'ui.bootstrap',
        'nya.bootstrap.select',
        'celestrak-services',
        'satnet-services',
        'broadcaster'
    ]
);

angular.module('ui-modalsc-controllers').controller('AddSCModalCtrl', [
    '$scope', '$log', '$modalInstance', 'satnetRPC', 'celestrak', 'broadcaster',
    function ($scope, $log, $modalInstance, satnetRPC, celestrak, broadcaster) {

        'use strict';

        $scope.sc = {
            identifier: '',
            callsign: '',
            tlegroup: '',
            tleid: ''
        };

        $scope.tlegroups = celestrak.CELESTRAK_SELECT_SECTIONS;
        $scope.tles = [];

        $scope.initTles = function (defaultOption) {
            satnetRPC.rCall('tle.celestrak.getResource', [defaultOption])
                .then(function (tleIds) {
                    $scope.tles = tleIds.tle_list.slice(0);
                    console.log('$scope.tles = ' + JSON.stringify($scope.tles));
                });
            $scope.sc.tlegroup = defaultOption;
        };
        $scope.groupChanged = function (value) {
            satnetRPC.rCall('tle.celestrak.getResource', [value.subsection])
                .then(function (tleIds) {
                    $scope.tles = tleIds.tle_list.slice(0);
                });
        };
        $scope.ok = function () {
            var newScCfg = [
                $scope.sc.identifier,
                $scope.sc.callsign,
                $scope.sc.tleid.spacecraft_tle_id
            ];
            satnetRPC.rCall('sc.add', newScCfg).then(function (data) {
                $log.info(
                    '[map-ctrl] SC added, id = ' + data.spacecraft_id
                );
                broadcaster.scAdded(data.spacecraft_id);
            });
            $modalInstance.close();
        };
        $scope.cancel = function () {
            $modalInstance.close();
        };
    }
]);

angular.module('ui-modalsc-controllers').controller('EditSCModalCtrl', [
    '$scope', '$log', '$modalInstance',
    'satnetRPC', 'celestrak', 'spacecraftId', 'broadcaster',
    function ($scope, $log, $modalInstance, satnetRPC, celestrak, spacecraftId, broadcaster) {
        'use strict';

        $scope.sc = {
            identifier: spacecraftId,
            callsign: '',
            tlegroup: '',
            tleid: '',
            savedTleId: ''
        };

        $scope.tlegroups = celestrak.CELESTRAK_SELECT_SECTIONS;
        $scope.tles = [];

        satnetRPC.rCall('sc.get', [spacecraftId]).then(function (data) {
            $scope.sc.identifier = spacecraftId;
            $scope.sc.callsign = data.spacecraft_callsign;
            $scope.sc.savedTleId = data.spacecraft_tle_id;
        });

        $scope.initTles = function (defaultOption) {
            satnetRPC.rCall('tle.celestrak.getResource', [defaultOption])
                .then(function (tleIds) {
                    $scope.tles = tleIds.tle_list.slice(0);
                });
            $scope.sc.tlegroup = defaultOption;
        };

        $scope.groupChanged = function (value) {
            satnetRPC.rCall('tle.celestrak.getResource', [value.subsection])
                .then(function (tleIds) {
                    $scope.tles = tleIds.tle_list.slice(0);
                });
        };
        $scope.update = function () {
            var newScCfg = {
                'spacecraft_id': spacecraftId,
                'spacecraft_callsign': $scope.sc.callsign,
                'spacecraft_tle_id': $scope.sc.tleid.id
            };
            satnetRPC.rCall(
                'sc.update',
                [spacecraftId, newScCfg]
            ).then(function (data) {
                $log.info('[map-ctrl] SC updated, id = ' + data);
                broadcaster.scUpdated(data);
            });
            $modalInstance.close();
        };
        $scope.cancel = function () {
            $modalInstance.close();
        };
        $scope.erase = function () {
            if (confirm('Delete this spacecraft?') === true) {
                satnetRPC.rCall('sc.delete', [spacecraftId]).then(function (data) {
                    $log.info(
                        '[map-ctrl] Spacecraft removed, id = ' +
                            JSON.stringify(data)
                    );
                    broadcaster.scRemoved(data);
                });
                $modalInstance.close();
            }
        };

    }
]);