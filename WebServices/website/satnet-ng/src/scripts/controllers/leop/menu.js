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
    'ui-leop-menu-controllers',
    [
        'ui.bootstrap',
        'satnet-services',
        'marker-models'
    ]
);

angular.module('ui-leop-menu-controllers').controller('LEOPGSMenuCtrl', [
    '$rootScope', '$scope', '$log', '$modal', 'satnetRPC', 'markers',
    function ($rootScope, $scope, $log, $modal, satnetRPC, markers) {
        'use strict';

        $scope.gsIds = [];

        $scope.panToGS = function (groundstation_id) {
            markers.panToGSMarker(groundstation_id).then(
                function (coordinates) {
                    $log.info(
                        '[menu-gs] Map panned to ' + JSON.stringify(coordinates)
                    );
                }
            );
        };

        $scope.addGroundStation = function () {
            var modalInstance = $modal.open({
                templateUrl: 'templates/leop/manageGroundStations.html',
                controller: 'ManageGSModalCtrl',
                backdrop: 'static',
                size: 'lg'
            });
            console.log('[leop-menu] Created modalInstance = ' + JSON.stringify(modalInstance));
        };
        $scope.refreshGSList = function () {
            satnetRPC.rCall('leop.gs.list', [$rootScope.leop_id])
                .then(function (data) {
                    if ((data !== null) && (data.leop_gs_inuse !== undefined)) {
                        $scope.gsIds = data.leop_gs_inuse.slice(0);
                    }
                });
        };
        $scope.refreshGSList();

    }
]);

angular.module('ui-leop-menu-controllers').controller('clusterMenuCtrl', [
    '$rootScope', '$scope', '$log', '$modal', 'satnetRPC', 'markers',
    function ($rootScope, $scope, $log, $modal, satnetRPC, markers) {
        'use strict';

        $scope.is_anonymous = $rootScope.is_anonymous;
        $scope.ufoIds = [];

        $scope.openManageCluster = function () {
            var modalInstance = $modal.open({
                templateUrl: 'templates/leop/manageCluster.html',
                controller: 'manageClusterModal',
                backdrop: 'static'
            });
            console.log(
                '[leop-menu] Created modalInstance = ' +
                    JSON.stringify(modalInstance)
            );
        };
        $scope.refreshSCList = function () {
            satnetRPC.rCall('leop.sc.list', [$rootScope.leop_id])
                .then(function (data) {
                    if (data !== null) {
                        $scope.scIds = data.slice(0);
                    }
                });
        };
        $scope.panToSC = function (groundstation_id) {
            markers.panToSCMarker(groundstation_id).then(
                function (coordinates) {
                    $log.info(
                        '[menu-gs] Map panned to ' + JSON.stringify(coordinates)
                    );
                }
            );
        };

    }
]);