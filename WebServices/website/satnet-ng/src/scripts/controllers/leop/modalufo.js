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
    .service('objectArrays', [
        function () {
            'use strict';

            /**
             * Function that checks whether the input parameters represent a
             * proper object array or not.
             * @param array Array of objects
             * @param property Property of the objects within the array used
             *                  during the comparison process
             */
            this.check = function (array, property) {
                if ((array === null) || (array.length === 0)) {
                    throw 'Array is empty';
                }
                if (array[0].hasOwnProperty(property) === false) {
                    throw 'Wrong property';
                }
            };

            /**
             * Function that searches for the give pair (property, value) within
             * this array of objects.
             * @param array Array of objects
             * @param property Property that belongs to all of the objects of
             *                  the array
             * @param value Value that the property equals to
             * @returns {number} Index of the object whose property has the
             *                      desired value
             */
            this.indexOf = function (array, property, value) {
                this.check(array, property);
                var i;
                for (i = 0; i < array.length; i += 1) {
                    if (array[i][property] === value) {
                        return i;
                    }
                }
                throw 'Pair not found in array, = (' +
                    property + ', ' + value + ')';
            };

            /**
             * Function that returns a tuple (index, object) with the object
             * whose property equals to the given value.
             * @param array Array of objects
             * @param property Property that belongs to all of the objects of
             *                  the array
             * @param value Value that the property equals to
             * @returns {{index: (number|Number), object: *}}
             */
            this.getObject = function (array, property, value) {
                var index = this.indexOf(array, property, value);
                return {
                    index: index,
                    object: array[index]
                };
            };

            /**
             * Function that returns the tuple (index, value) that has the
             * biggest value within the given array.
             * @param array Array for the search.
             * @param property The property of the object for the comparison.
             * @returns {{index: number, value: number}}
             */
            this.findMaxTuple = function (array, property) {
                this.check(array, property);

                var i, max_value = -1, max_index = 0;
                for (i = 0; i < array.length; i += 1) {
                    if (array[i][property] > max_value) {
                        max_value = array[i][property];
                        max_index = i;
                    }
                }

                return {
                    index: max_index,
                    value: max_value
                };

            };

        }
    ])
    .controller('manageClusterModal', [
        '$rootScope', '$scope', '$log', '$modalInstance', 'objectArrays', 'MAX_UFOS',
        function ($rootScope, $scope, $log, $modalInstance, objectArrays, MAX_UFOS) {
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
                    },
                    identified_objects: {}
                }
            );

            $scope.init = function () {
                $scope.cluster.identifier = $rootScope.leop_id;
            };

            $scope.add = function () {
                var id_ufos, id_identified, id;
                id_ufos = ($scope.cluster.ufos.length === 0) ? 0
                    : objectArrays.findMaxTuple($scope.cluster.ufos, 'object_id').value;
                id_identified = ($scope.cluster.identified.length === 0) ? 0
                    : objectArrays.findMaxTuple($scope.cluster.identified, 'object_id').value;
                id = (id_ufos > id_identified) ? id_ufos + 1 : id_identified + 1;
                $scope.cluster.ufos.push({ object_id: id });
            };

            $scope.remove = function () {
                $scope.cluster.ufos.splice([$scope.cluster.ufos.length - 1], 1);
            };

            /**
             * Turns an UFO into an object who has been temporary identified.
             * @param object_id Identifier of the object
             */
            $scope.identify = function (object_id) {

                var idx_obj = objectArrays.getObject(
                    $scope.cluster.ufos,
                    'object_id',
                    object_id
                );

                $log.info(
                    '[modal-ufo] <Object#' +
                        object_id + '> promted to the identified objects list.'
                );

                angular.extend(
                    idx_obj.object,
                    {
                        tle: {
                            l1: '',
                            l2: ''
                        },
                        alias: ''
                    }
                );
                $scope.cluster.identified.push(idx_obj.object);
                $scope.cluster.ufos.splice(idx_obj.index, 1);

            };

            /**
             * "Forgets" the temporal identity of a given UFO.
             * @param object_id Identifier of the object
             */
            $scope.forget = function (object_id) {

                if (confirm('Are you sure that you want to return <Object#' +
                        object_id + '> back to the UFO list?') === false) {
                    $log.warn(
                        '[modal-ufo] <Object#' +
                            object_id + '> kept in the identified objects list.'
                    );
                    return;
                }

                var idx_obj = objectArrays.getObject(
                    $scope.cluster.identified,
                    'object_id',
                    object_id
                );

                $log.info(
                    '[modal-ufo] <Object#' +
                        object_id + '> back in the UFO list.'
                );

                $scope.cluster.ufos.push(idx_obj.object);
                $scope.cluster.identified.splice(idx_obj.index, 1);

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