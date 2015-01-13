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
        'ui.bootstrap',
        'satnet-services'
    ]
);

angular.module('ui-leop-modalufo-controllers')
    .constant('MAX_UFOS', 24)
    .constant('MAX_COLUMNS', 4)
    .service('objectArrays', [
        function () {
            'use strict';

            /**
             * Function that checks whether the input parameters represent a
             * proper object array or not.
             * @param array Array for the operation
             * @param property The property for the operation
             */
            this.check = function (array, property) {
                if (array === null) { throw 'Array is null'; }
                if (array.length === 0) { return true; }
                if (array[0].hasOwnProperty(property) === false) {
                    throw 'Wrong property';
                }
                return true;
            };

            /**
             * Function that searches for the give pair (property, value) within
             * this array of objects.
             * @param array Array for the operation
             * @param property The property for the operation
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
             * @param array Array for the operation
             * @param property The property for the operation
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
             * @param array Array for the operation
             * @param property The property for the operation
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

            /**
             * Function that returns the same array but changing the strings of
             * the values at the given property by the result of parseInt'ing
             * them.
             * @param array Array for the operation
             * @param property The property for the operation
             * @returns {*}
             */
            this.parseInt = function (array, property) {
                this.check(array, property);
                var i;
                for (i = 0; i < array.length; i += 1) {
                    array[i][property] = parseInt(array[i][property], 10);
                }
                return array;
            };

            /**
             * Splits a given array into a matrix of arrays whose maximum
             * length is the @param max_columms number given as a second
             * parameter.
             * @param array The array to be split
             * @param max_columns Maximum number of columns
             * @returns {*}
             */
            this.split = function (array, max_columns) {

                if (array === null) {
                    throw 'array is null';
                }
                if (max_columns < 1) {
                    throw 'max_columns should be > 1, actual = ' + max_columns;
                }
                if (array === undefined) {
                    return [];
                }
                if (array.length <= max_columns) { return array; }

                var i, j, columns, index,
                    rowsNum = Math.ceil(array.length / max_columns),
                    rows = new Array(rowsNum);

                for (i = 0; i < rowsNum; i += 1) {
                    columns = [];
                    for (j = 0; j < max_columns; j += 1) {
                        index = i * max_columns + j;
                        if (index < array.length) {
                            columns[j] = array[index];
                        } else { break; }
                    }
                    rows[i] = columns;
                }

                return rows;

            };

            /**
             * Iterates over the objects of the given array and adds the
             * pair (key, value) to each of those items.
             * @param array Array over wich to iterate
             * @param key Name of the property
             * @param value Value of the property
             * @returns {*}
             */
            this.addProperty = function (array, key, value) {

                if (array === null) { throw 'Array is null'; }
                if (array.length === 0) { return true; }
                if (key === null) { throw 'Key is null'; }
                if (key.length === 0) { throw 'Key is blank'; }
                if (value === null) { throw 'Value is null'; }
                if (array[0].hasOwnProperty(key) === true) {
                    throw 'Property already defined, k = ' + key;
                }
                var i;

                for (i = 0; i < array.length; i += 1) {
                    array[i][key] = value;
                }

                return array;

            };

        }
    ])
    .controller('manageClusterModal', [
        '$rootScope', '$scope', '$log', '$modalInstance',
        'satnetRPC', 'objectArrays', 'MAX_UFOS',
        function (
            $rootScope,
            $scope,
            $log,
            $modalInstance,
            satnetRPC,
            objectArrays,
            MAX_UFOS
        ) {
            'use strict';

            $scope.cluster = {};

            $scope.init = function () {
                var scope = $scope;
                satnetRPC.rCall('leop.cfg', [$rootScope.leop_id])
                    .then(function (data) {
                        console.log(
                            '[modal-ufo] cluster cfg = ' + JSON.stringify(data)
                        );
                        objectArrays.parseInt(data.ufos, 'object_id');
                        angular.extend($scope.cluster, data);
                        scope.cluster.max_ufos = MAX_UFOS;
                        //scope.editing = {};
                        objectArrays.addProperty(
                            scope.cluster.identified,
                            'editing',
                            false
                        );

                    });
            };

            $scope.add = function () {

                var id_ufos, id_identified, id;

                id_ufos = ($scope.cluster.ufos.length === 0) ? 0
                    : objectArrays.findMaxTuple($scope.cluster.ufos, 'object_id').value;
                id_identified = ($scope.cluster.identified.length === 0) ? 0
                    : objectArrays.findMaxTuple($scope.cluster.identified, 'object_id').value;
                id = (id_ufos > id_identified) ? id_ufos + 1 : id_identified + 1;

                satnetRPC.rCall('leop.ufo.add', [$rootScope.leop_id, id])
                    .then(function (data) {
                        $log.info('[modal-ufo] New ufo, id = ' + data);
                        $scope.cluster.ufos.push({ object_id: id });
                    });

            };

            $scope.remove = function () {

                if ($scope.cluster.ufos.length === 0) {
                    $log.warn('[modal-ufo] removing from empty ufos?');
                    return;
                }

                var i = $scope.cluster.ufos.length - 1,
                    id = $scope.cluster.ufos[i].object_id;

                satnetRPC.rCall('leop.ufo.remove', [$rootScope.leop_id, id])
                    .then(function (data) {
                        $log.info('[modal-ufo] Removed ufo, id = ' + data);
                        $scope.cluster.ufos.splice(i, 1);
                    });

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
                        object_id + '> promoted to the identified list.'
                );

                angular.extend(
                    idx_obj.object,
                    { tle: { l1: '', l2: '' }, callsign: '', editing: true }
                );

                $scope.cluster.identified.push(idx_obj.object);
                $scope.cluster.ufos.splice(idx_obj.index, 1);
                /*
                $scope.editing[object_id] = {
                    editing: true,
                    tle: { l1: '', l2: '' },
                    callsign: ''
                };
                */

            };

            $scope.edit = function (object_id) {
                $scope.editing[object_id].editing = true;
            };

            $scope.save_edit = function (object_id) {

                console.log('>>> cs = ' + $scope.editing[object_id].callsign);
                console.log('>>> tle_l1 = ' + $scope.editing[object_id].tle.l1);
                console.log('>>> tle_l2 = ' + $scope.editing[object_id].tle.l2);

                /**/
                satnetRPC.rCall(
                    'leop.ufo.identify',
                    [
                        $rootScope.leop_id,
                        object_id,
                        $scope.editing[object_id].callsign,
                        $scope.editing[object_id].tle.l1,
                        $scope.editing[object_id].tle.l2
                    ]
                )
                    .then(function (data) {
                        $log.info(
                            '[modal-ufo] <Object#' + data + '> IDENTIFIED!'
                        );
                    });
                /**/
                $scope.editing[object_id].editing = false;
            };

            $scope.cancel_edit = function (object_id) {
                $scope.editing[object_id].editing = false;
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
                    ),
                    scope = $scope;

                scope.cluster.ufos.push(idx_obj.object);
                scope.cluster.identified.splice(idx_obj.index, 1);

                /**/
                satnetRPC.rCall(
                    'leop.ufo.forget',
                    [$rootScope.leop_id, object_id]
                )
                    .then(function (data) {
                        $log.info(
                            '[modal-ufo] <Object#' + data + '> back as a UFO.'
                        );

                    });
                /**/

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