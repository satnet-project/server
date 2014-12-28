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
    'ui-menu-controllers',
    ['ui.bootstrap', 'satnet-services']
);

angular.module('ui-menu-controllers').controller('GSMenuCtrl', [
    '$scope', '$modal', 'satnetRPC',
    function ($scope, $modal, satnetRPC) {

        'use strict';

        $scope.gsIds = [];
        $scope.addGroundStation = function () {
            var modalInstance = $modal.open({
                templateUrl: '/static/scripts/src/templates/addGroundStation.html',
                controller: 'AddGSModalCtrl',
                backdrop: 'static'
            });
            console.log('Created modalInstance = ' + modalInstance);
        };
        $scope.editGroundStation = function (g) {
            var modalInstance = $modal.open({
                templateUrl: '/static/scripts/src/templates/editGroundStation.html',
                controller: 'EditGSModalCtrl',
                backdrop: 'static',
                resolve: { groundstationId: function () {
                    return g;
                } }
            });
            console.log('Created modalInstance = ' + modalInstance);
        };
        $scope.refreshGSList = function () {
            satnetRPC.rCall('gs.list', []).then(function (data) {
                if (data !== null) {
                    $scope.gsIds = data.slice(0);
                }
            });
        };
        $scope.refreshGSList();

    }
]);

angular.module('ui-menu-controllers').controller('SCMenuCtrl', [
    '$scope', '$modal', 'satnetRPC',
    function ($scope, $modal, satnetRPC) {

        'use strict';

        $scope.scIds = [];
        $scope.addSpacecraft = function () {
            var modalInstance = $modal.open({
                templateUrl: '/static/scripts/src/templates/addSpacecraft.html',
                controller: 'AddSCModalCtrl',
                backdrop: 'static'
            });
            console.log('Created modalInstance = ' + modalInstance);
        };
        $scope.editSpacecraft = function (s) {
            var modalInstance = $modal.open({
                templateUrl: '/static/scripts/src/templates/editSpacecraft.html',
                controller: 'EditSCModalCtrl',
                backdrop: 'static',
                resolve: { spacecraftId: function () {
                    return s;
                } }
            });
            console.log('Created modalInstance = ' + modalInstance);
        };
        $scope.refreshSCList = function () {
            satnetRPC.rCall('sc.list', []).then(function (data) {
                if (data !== null) {
                    console.log('sc.list >>> data = ' + JSON.stringify(data));
                    $scope.scIds = data.slice(0);
                }
            });
        };
        $scope.refreshSCList();

    }
]);

angular.module('ui-menu-controllers').controller('ExitMenuCtrl', [
    '$scope', '$log',
    function ($scope, $log) {
        'use strict';
        $scope.home = function () {
            $log.info('Exiting...');
        };
    }
]);