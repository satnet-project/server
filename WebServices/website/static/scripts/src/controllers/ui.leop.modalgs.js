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
    'ui-leop-modalgs-controllers',
    []
);

/*
    [
        'ui.bootstrap',
        'nya.bootstrap.select',
        'leaflet-directive',
        'common',
        'x-satnet-services',
        'broadcaster'
    ]
);
*/

angular.module('ui-leop-modalgs-controllers')
    .controller('ManageGSModalCtrl', [
        '$scope',
        '$modalInstance',
        function (
            $scope,
            $modalInstance
        ) {

            'use strict';

            $scope.gsIds = {};
            $scope.gsIds.aItems = [];
            $scope.gsIds.uItems = [];

            $scope.gsIds.toAdd = [];
            $scope.gsIds.toRemove = [];

            $scope.init = function () {
                console.log('init');
                /*
                xSatnetRPC.readLEOPGs($rootScope.leop_id)
                    .then(function (data) {
                        console.log('leop.gs.list, data = ' + JSON.stringify(data));
                        if (data === null) { return; }
                        $scope.gsIds = data;
                    });
                */
            };

            $scope.selectGs = function () {
                console.log('selectGs');
                /*
                var i, item;
                console.log('>>> aItems = ' + JSON.stringify($scope.gsIds.aItems));
                console.log('>>> toAdd = ' + JSON.stringify($scope.gsIds.toAdd));
                console.log('>>> leop_gs_a = ' + JSON.stringify($scope.gsIds.leop_gs_available));
                console.log('>>> leop_gs_u = ' + JSON.stringify($scope.gsIds.leop_gs_inuse));

                if ($scope.gsIds.toAdd === undefined) {
                    $scope.gsIds.toAdd = [];
                }

                for (i = 0; i < $scope.gsIds.aItems.length; i += 1) {
                    item = $scope.gsIds.aItems[i];
                    $scope.gsIds.leop_gs_available.splice(
                        $scope.gsIds.leop_gs_available.indexOf(item),
                        1
                    );
                    if ($scope.gsIds.toAdd.indexOf(item) < 0) {
                        $scope.gsIds.toAdd.push(item);
                    }
                    if ($scope.gsIds.leop_gs_inuse.indexOf(item) < 0) {
                        $scope.gsIds.leop_gs_inuse.push(item);
                    }
                }

                $scope.gsIds.aItems = [];
                console.log('<<< aItems = ' + JSON.stringify($scope.gsIds.aItems));
                console.log('<<< toAdd = ' + JSON.stringify($scope.gsIds.toAdd));
                console.log('<<< leop_gs_a = ' + JSON.stringify($scope.gsIds.leop_gs_available));
                console.log('<<< leop_gs_u = ' + JSON.stringify($scope.gsIds.leop_gs_inuse));
                */
            };

            $scope.unselectGs = function () {
                console.log('unselectGs');
                /*
                var i, item;
                console.log('>>> uItems = ' + JSON.stringify($scope.gsIds.uItems));
                console.log('>>> toRemove = ' + JSON.stringify($scope.gsIds.toRemove));
                console.log('>>> leop_gs_u = ' + JSON.stringify($scope.gsIds.leop_gs_inuse));
                if ($scope.gsIds.toRemove === undefined) {
                    $scope.gsIds.toRemove = [];
                }

                for (i = 0; i < $scope.gsIds.uItems.length; i += 1) {
                    item = $scope.gsIds.uItems[i];
                    $scope.gsIds.leop_gs_inuse.splice(
                        $scope.gsIds.leop_gs_inuse.indexOf(item),
                        1
                    );
                    if ($scope.gsIds.toRemove.indexOf(item) < 0) {
                        $scope.gsIds.toRemove.push(item);
                    }
                    if ($scope.gsIds.leop_gs_available.indexOf(item) < 0) {
                        $scope.gsIds.leop_gs_available.push(item);
                    }
                }

                $scope.gsIds.uItems = [];
                console.log('<<< uItems = ' + JSON.stringify($scope.gsIds.uItems));
                console.log('<<< toRemove = ' + JSON.stringify($scope.gsIds.toRemove));
                console.log('<<< leop_gs_u = ' + JSON.stringify($scope.gsIds.leop_gs_inuse));
                */
            };

            $scope.ok = function () {
                console.log('ok');
                /*
                var a_ids = [], r_ids = [], i;
                for (i = 0; i < $scope.gsIds.toAdd.length; i += 1) {
                    a_ids.push($scope.gsIds.toAdd[i].groundstation_id);
                }
                for (i = 0; i < $scope.gsIds.toRemove.length; i += 1) {
                    r_ids.push($scope.gsIds.toRemove[i].groundstation_id);
                }
                satnetRPC.rCall('leop.gs.add', [a_ids]).then(
                    function (data) {
                        console.log(
                            '>>> updated LEOP = ' + JSON.stringify(data)
                        );
                    }
                );
                satnetRPC.rCall('leop.gs.remove', [r_ids]).then(
                    function (data) {
                        console.log(
                            '>>> updated LEOP = ' + JSON.stringify(data)
                        );
                    }
                );
                */
            };

            $scope.cancel = function () {
                $modalInstance.close();
            };

            $scope.init();

        }
    ]);