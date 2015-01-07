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
    'ui-leop-modalufo-controllers',
    [
        'ui.bootstrap'
    ]
);

angular.module('ui-leop-modalufo-controllers')
    .constant('MAX_UFOS', 24)
    .controller('manageClusterModal', [
        '$rootScope', '$scope', '$log', '$modalInstance', 'MAX_UFOS',
        function ($rootScope, $scope, $log, $modalInstance, MAX_UFOS) {
            'use strict';

            angular.extend(
                $scope,
                {
                    cluster: {
                        identifier: '',
                        tle: { l1: '', l2: '' },
                        max_ufos: MAX_UFOS,
                        ufos: [],
                        identified: []
                    }
                }
            );

            $scope.init = function () {
                $scope.cluster.identifier = $rootScope.leop_id;
            };

            $scope.add = function () {
                var id;
                if ($scope.cluster.ufos.length === 0) {
                    id = 0;
                } else {
                    id = $scope.cluster.ufos[$scope.cluster.ufos.length - 1].object_id + 1;
                }
                $scope.cluster.ufos.push({
                    object_id: id
                });
            };
            $scope.remove = function () {
                $scope.cluster.ufos.splice([$scope.cluster.ufos.length - 1], 1);
            };

            $scope.ok = function () {
                $log.info('[modal-ufo] cfg changed');
                $modalInstance.close();
            };
            $scope.cancel = function () {
                $modalInstance.close();
            };

            $scope.init();

        }
    ]);