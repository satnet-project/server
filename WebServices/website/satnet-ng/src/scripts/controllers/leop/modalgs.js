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
    [ 'broadcaster', 'satnet-services' ]
);

/**
 * Angular module with the Modal GS controllers.
 */
angular.module('ui-leop-modalgs-controllers')
    .controller('ManageGSModalCtrl', [
        '$rootScope',
        '$scope',
        '$modalInstance',
        'broadcaster',
        'satnetRPC',
        function (
            $rootScope,
            $scope,
            $modalInstance,
            broadcaster,
            satnetRPC
        ) {

            'use strict';

            $scope.gsIds = {};
            $scope.gsIds.aItems = [];
            $scope.gsIds.uItems = [];

            $scope.gsIds.toAdd = [];
            $scope.gsIds.toRemove = [];

            $scope.ll_changed = false;

            $scope.init = function () {
                console.log('init, leop_id = ' + $rootScope.leop_id);
                satnetRPC.readAllLEOPGS($rootScope.leop_id)
                    .then(function (data) {
                        console.log('leop.gs.list, data = ' + JSON.stringify(data));
                        if (data === null) { return; }
                        $scope.gsIds = data;
                    });
            };

            $scope.selectGs = function () {
                var i, item;

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
            };

            $scope.unselectGs = function () {
                var i, item;
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
            };

            $scope.ok = function () {

                var a_ids = [], r_ids = [], i, gs_id;

                if ($scope.gsIds.toAdd !== undefined) {
                    for (i = 0; i < $scope.gsIds.toAdd.length; i += 1) {
                        gs_id = $scope.gsIds.toAdd[i].groundstation_id;
                        a_ids.push(gs_id);
                        broadcaster.gsAdded(gs_id);
                    }
                    satnetRPC.rCall(
                        'leop.gs.add',
                        [$rootScope.leop_id, a_ids]
                    ).then(
                        function (data) {
                            console.log(
                                '>>> updated LEOP = ' + JSON.stringify(data)
                            );
                        }
                    );
                }

                if ($scope.gsIds.toRemove !== undefined) {
                    for (i = 0; i < $scope.gsIds.toRemove.length; i += 1) {
                        gs_id = $scope.gsIds.toRemove[i].groundstation_id;
                        r_ids.push(gs_id);
                        broadcaster.gsRemoved(gs_id);
                    }
                    satnetRPC.rCall(
                        'leop.gs.remove',
                        [$rootScope.leop_id, r_ids]
                    ).then(
                        function (data) {
                            console.log(
                                '>>> updated LEOP = ' + JSON.stringify(data)
                            );
                        }
                    );
                }

                $modalInstance.close();

            };

            $scope.cancel = function () {
                $modalInstance.close();
            };

            $scope.init();

        }
    ]);