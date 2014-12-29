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
    ['ui.bootstrap', 'satnet-services']
);

angular.module('ui-leop-menu-controllers').controller('LEOPGSMenuCtrl', [
    '$rootScope', '$scope', '$modal', 'satnetRPC',
    function ($rootScope, $scope, $modal, satnetRPC) {

        'use strict';

        $scope.gsIds = [];

        $scope.addGroundStation = function () {
            var modalInstance = $modal.open({
                templateUrl: '/static/src/templates/leop/manageGroundStations.html',
                controller: 'ManageGSModalCtrl',
                backdrop: 'static'
            });
            console.log('Created modalInstance = ' + modalInstance);
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

angular.module('ui-leop-menu-controllers').controller('UFOMenuCtrl', [
    '$scope', '$modal', 'satnetRPC',
    function ($scope, $modal, satnetRPC) {

        'use strict';

        $scope.ufoIds = [];
        $scope.addUFO = function () {
            var modalInstance = $modal.open({
                templateUrl: '/static/src/templates/leop/manageUFO.html',
                controller: 'ManageUFOCtrl',
                backdrop: 'static'
            });
            console.log('Created modalInstance = ' + modalInstance);
        };
        $scope.refreshUFOList = function () {
            satnetRPC.rCall('leop.ufo.list', []).then(function (data) {
                if (data !== null) {
                    console.log(
                        'leop.ufo.list >>> data = ' + JSON.stringify(data)
                    );
                    $scope.scIds = data.slice(0);
                }
            });
        };
        //$scope.refreshUFOList();

    }
]);