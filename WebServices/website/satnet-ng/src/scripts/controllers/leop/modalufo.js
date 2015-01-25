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
angular.module('ui-leop-modalufo-controllers', [
    'ui.bootstrap', 'satnet-services'
]);

angular.module('ui-leop-modalufo-controllers')
    .constant('CLUSTER_CFG_UPDATED_EV', 'cluster-cfg-updated')
    .constant('MAX_OBJECTS', 12)
    .constant('MAX_COLUMNS', 4)
    .service('oArrays', [
        function () {
            'use strict';

            /**
             * Function that checks whether the input parameters represent a
             * proper object array or not.
             * @param array Array for the operation
             * @param property The property for the operation
             */
            this.check = function (array, property) {
                if (!array) {
                    throw 'Array is invalid';
                }
                if (array.length === 0) {
                    return true;
                }
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
                if (array.length <= max_columns) {
                    return array;
                }

                var i, j, columns, index,
                    rowsNum = Math.ceil(array.length / max_columns),
                    rows = new Array(rowsNum);

                for (i = 0; i < rowsNum; i += 1) {
                    columns = [];
                    for (j = 0; j < max_columns; j += 1) {
                        index = i * max_columns + j;
                        if (index < array.length) {
                            columns[j] = array[index];
                        } else {
                            break;
                        }
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

                if (array === null) {
                    throw 'Array is null';
                }
                if (array.length === 0) {
                    return true;
                }
                if (key === null) {
                    throw 'Key is null';
                }
                if (key.length === 0) {
                    throw 'Key is blank';
                }
                if (value === null) {
                    throw 'Value is null';
                }
                if (array[0].hasOwnProperty(key) === true) {
                    throw 'Property already defined, k = ' + key;
                }
                var i;

                for (i = 0; i < array.length; i += 1) {
                    array[i][key] = value;
                }

                return array;

            };

            /**
             * This function inserts the given element into the array in
             * accordance with the insertion algorithm. The array list is
             * suppossed to be sorted before hand. For the comparison, it
             * uses the <key> property that all the elements of the array
             * should have.
             *
             * @param array Already sorted array
             * @param property Object's property for comparison
             * @param element The element to be inserted
             * @returns {*}
             */
            this.insertSorted = function (array, property, element) {
                this.check(array, property);
                if (element === null) {
                    throw 'Element is null';
                }
                if (element.hasOwnProperty(property) === false) {
                    throw 'Invalid element';
                }
                var i;

                for (i = 0; i < array.length; i += 1) {
                    if (array[i][property] > element[property]) {
                        break;
                    }
                }

                array.splice(i, 0, element);
                return array;

            };

            /**
             * Function that converts an array of objects into a dictionary
             * where the objects can be accessed using as a key the value
             * for their own property. The property chosen is the one whose
             * name was given as a parameter to this function. The property is
             * not erased from the object.
             *
             * @param array Array to be converted
             * @param property Property whose value is used as a key
             * @returns {{}}
             */
            this.array2dict = function (array, property) {
                this.check(array, property);
                if (!property) {
                    throw 'Property is null';
                }
                var obj = {}, dict = {}, key;

                angular.forEach(array, function (i) {
                    angular.extend(obj, i);
                    key = i[property];
                    dict[key] = obj;
                    obj = {};
                });

                return dict;

            };

        }
    ])
    .service('xDicts', [
        function () {
            'use strict';

            /**
             * Function that checks the validity of the parameters passed to
             * most of the functions that this service offers.
             * @param dict The dictionary passed as an argument
             * @param property The property passed as an argument
             * @returns {boolean} 'true' if the operation was succesful
             */
            this.check = function (dict, property) {
                if (!dict) {
                    throw '<Dict> is invalid';
                }
                if (!property) {
                    throw '<property> is invalid';
                }
                return true;
            };

            /**
             * Function that finds the pair key, object of this dictionry whose
             * value for the specified property is the biggest from amongst all
             * in the same dictionary.
             * @param dict The dictionary
             * @param property The property
             * @returns {*[]}
             */
            this.findMaxTuple = function (dict, property) {
                this.check(dict, property);
                var k, max_k, v = 0, max_v = 0, size = 0;
                for (k in dict) {
                    if (dict.hasOwnProperty(k)) {
                        size += 1;
                        v = dict[k][property];
                        if (v < max_v) {
                            continue;
                        }
                        max_v = v;
                        max_k = k;
                    }
                }
                if (size === 0) {
                    return [undefined, 0];
                }
                return [max_k, max_v];
            };

            /**
             * Checks whether this dictionary is empty or not.
             * @param dict The dictionary
             * @returns {boolean} 'true' if the dictionary is empty
             */
            this.isEmpty = function (dict) {
                this.check(dict, 'any');
                var k;
                for (k in dict) {
                    if (dict.hasOwnProperty(k)) {
                        return false;
                    }
                }
                return true;
            };

            /**
             * Returns the length of this dictionary.
             * @param dict The dictionary
             * @returns {number} Length of the dictionary
             */
            this.size = function (dict) {
                this.check(dict, 'any');
                var k, length = 0;
                for (k in dict) {
                    if (dict.hasOwnProperty(k)) {
                        length += 1;
                    }
                }
                return length;
            };

        }
    ])
    .controller('manageClusterModal', [
        '$rootScope', '$scope', '$log', '$modalInstance',
        'broadcaster',
        'satnetRPC', 'oArrays', 'xDicts',
        'MAX_OBJECTS', 'CLUSTER_CFG_UPDATED_EV',
        function (
            $rootScope,
            $scope,
            $log,
            $modalInstance,
            broadcaster,
            satnetRPC,
            oArrays,
            xDicts,
            MAX_OBJECTS,
            CLUSTER_CFG_UPDATED_EV
        ) {
            'use strict';

            $scope.is_anonymous = $rootScope.is_anonymous;
            $scope.cluster = {};

            $scope._initData = function () {
                satnetRPC.rCall('leop.cfg', [$rootScope.leop_id]).then(
                    function (data) {
                        console.log(
                            '[modal-ufo] leop cfg = ' + JSON.stringify(data)
                        );
                        $scope.cluster.identifier = data.identifier;
                        $scope.cluster.sc_identifier = data.sc_identifier;
                        $scope.cluster.old_tle_l1 = data.tle_l1;
                        $scope.cluster.old_tle_l2 = data.tle_l2;
                        $scope.cluster.tle_l1 = data.tle_l1;
                        $scope.cluster.tle_l2 = data.tle_l2;
                        $scope.cluster.date = data.date;
                        $scope.cluster.max_objects = MAX_OBJECTS;
                        $scope.cluster.no_objects = 0;
                        $scope.cluster.edit = false;

                        oArrays.parseInt(data.ufos, 'object_id');
                        $scope.cluster.ufos =
                            $scope._objArr2Dict(data.ufos);
                        $scope.cluster.no_ufos = $scope._ufosSize();

                        $scope.cluster.editing = {};
                        $scope.cluster.no_editing = 0;

                        $scope.cluster.identified =
                            $scope._objArr2Dict(data.identified);
                        $scope.cluster.no_identified = $scope._identifiedSize();
                    }
                );
            };

            $scope._initListeners = function () {
                $scope.$on(
                    broadcaster.LEOP_UPDATED_EVENT,
                    function (event, id) {
                        console.log(
                            '[modalufo] ev = ' + event + ', id = ' + id
                        );
                        $scope._initData();
                    }
                );
            };

            $scope.init = function () {
                $scope._initData();
                $scope._initListeners();
            };

            $scope._objArr2Dict = function (array) {
                return oArrays.array2dict(array, 'object_id');
            };
            $scope._biggestUfo = function () {
                var array = $scope.cluster.ufos,
                    max = xDicts.findMaxTuple(array, 'object_id');
                return max[1];
            };
            $scope._biggestIded = function () {
                var array = $scope.cluster.identified,
                    max = xDicts.findMaxTuple(array, 'object_id');
                return max[1];
            };
            $scope._nextObjectId = function () {
                var id_ufos = $scope._biggestUfo(),
                    id_identified = $scope._biggestIded();
                return (id_ufos > id_identified)
                    ? parseInt(id_ufos, 10) + 1
                    : parseInt(id_identified, 10) + 1;
            };

            $scope._isUfosEmpty = function () {
                return xDicts.isEmpty($scope.cluster.ufos);
            };
            $scope._ufosSize = function () {
                return xDicts.size($scope.cluster.ufos);
            };
            $scope._addUfo = function (object_id) {
                $scope.cluster.ufos[object_id] = { 'object_id': object_id };
                $scope.cluster.no_ufos += 1;
            };
            $scope._removeUfo = function (object_id) {
                delete $scope.cluster.ufos[object_id];
                $scope.cluster.no_ufos -= 1;
            };
            $scope._getUfo = function (object_id) {
                return $scope.cluster.ufos[object_id];
            };

            $scope._addEditingUfo = function (object_id) {
                if ($scope.is_anonymous) { return; }
                $scope.cluster.editing[object_id] = {
                    object_id: object_id,
                    sc_identifier: '',
                    tle_l1: '',
                    tle_l2: '',
                    callsign: '',
                    edit: true,
                    past: 'ufo'
                };
                $scope.cluster.no_editing += 1;
            };
            $scope._addEditingIded = function (object_id, cfg) {
                $scope.cluster.editing[object_id] = {
                    object_id: object_id,
                    sc_identifier: cfg.sc_id,
                    tle_l1: cfg.tle_l1,
                    tle_l2: cfg.tle_l2,
                    callsign: cfg.callsign,
                    edit: true,
                    past: 'identified'
                };
                $scope.cluster.no_editing += 1;
            };
            $scope._removeEditing = function (object_id) {
                delete $scope.cluster.editing[object_id];
                $scope.cluster.no_editing -= 1;
            };
            $scope._getEditing = function (object_id) {
                return $scope.cluster.editing[object_id];
            };
            $scope._disableEditing = function (object_id) {
                $scope.cluster.editing[object_id].edit = false;
            };

            $scope._identifiedSize = function () {
                return xDicts.size($scope.cluster.identified);
            };
            $scope._addIdentified = function (object_id, cfg) {
                $scope.cluster.identified[object_id] = {
                    object_id: object_id,
                    sc_identifier: cfg.sc_id,
                    tle_l1: cfg.tle_l1,
                    tle_l2: cfg.tle_l2,
                    callsign: cfg.callsign
                };
                $scope.cluster.no_identified += 1;
            };
            $scope._removeIdentified = function (object_id) {
                delete $scope.cluster.identified[object_id];
                $scope.cluster.no_identified -= 1;
            };
            $scope._getIdentified = function (object_id) {
                return $scope.cluster.identified[object_id];
            };

            $scope._updateNoObjects = function () {
                $scope.cluster.no_objects =
                    $scope.cluster.no_ufos +
                    $scope.cluster.no_editing +
                    $scope.cluster.no_identified;
            };

            $scope.add = function () {
                var next_id = $scope._nextObjectId(), scope = $scope;
                satnetRPC.rCall('leop.ufo.add', [$rootScope.leop_id, next_id])
                    .then(function (data) {
                        $log.info('[modal-ufo] New ufo, id = ' + data);
                        scope._addUfo(next_id);
                    });
            };

            $scope.remove = function () {
                var id = $scope._biggestUfo(), scope = $scope;
                satnetRPC.rCall('leop.ufo.remove', [$rootScope.leop_id, id])
                    .then(function (data) {
                        $log.info('[modal-ufo] Removed ufo, id = ' + data);
                        scope._removeUfo(id);
                    });
            };

            $scope.editingUfo = function (object_id) {
                $scope._addEditingUfo(object_id);
                $scope._removeUfo(object_id);
            };

            $scope.editingIded = function (object_id) {
                if ($scope.is_anonymous) { return; }
                var object = $scope._getIdentified(object_id);
                $scope._addEditingIded(object_id, object);
                $scope._removeIdentified(object_id);
            };

            $scope.cancel = function (object_id) {
                var object = $scope._getEditing(object_id);
                if (object.past === 'ufo') {
                    $scope._addUfo(object_id);
                } else {
                    $scope._addIdentified(object_id, object);
                }
                $scope._removeEditing(object_id);
            };

            $scope.save = function (object_id) {
                var object = $scope._getEditing(object_id);
                $scope._disableEditing(object_id);
                if (object.past === 'ufo') {
                    $scope._saveUfo(object_id, object);
                } else {
                    $scope._saveIded(object_id, object);
                }
            };

            $scope._saveUfo = function (object_id, object) {
                var err_msg = '[modal-ufo] Wrong configuration, ex = ';
                satnetRPC.rCall(
                    'leop.ufo.identify',
                    [
                        $rootScope.leop_id,
                        object_id,
                        object.callsign,
                        object.tle_l1,
                        object.tle_l2
                    ]
                ).then(
                    function (data) {
                        $log.info(
                            '[modal-ufo] <Object#' + data.object_id + '> SAVED!'
                        );
                        object.sc_identifier = data.sc_identifier;
                        $scope._addIdentified(object_id, object);
                        $scope._removeEditing(object_id);
                        broadcaster.scAdded(object.sc_identifier);
                    },
                    function (data) {
                        err_msg += JSON.stringify(data);
                        $log.warn(err_msg);
                        if (alert(err_msg) === false) {
                            $log.warn(err_msg);
                        }
                    }
                );
            };

            $scope._saveIded = function (object_id, object) {
                var err_msg = '[modal-ufo] Wrong configuration, ex = ';
                satnetRPC.rCall(
                    'leop.ufo.update',
                    [
                        $rootScope.leop_id,
                        object_id,
                        object.callsign,
                        object.tle_l1,
                        object.tle_l2
                    ]
                ).then(
                    function (data) {
                        $log.info(
                            '[modal-ufo] <Object#' + data.object_id + '> SAVED!'
                        );
                        object.sc_identifier = data.sc_identifier;
                        $scope._addIdentified(object_id, object);
                        $scope._removeEditing(object_id);
                        broadcaster.scUpdated(object.sc_identifier);
                    },
                    function (data) {
                        err_msg += JSON.stringify(data);
                        $log.warn(err_msg);
                        if (alert(err_msg) === false) {
                            $log.warn(err_msg);
                        }
                    }
                );
            };

            $scope.forget = function (object_id) {
                var ask_msg = 'Are you sure that you want to return <Object#' +
                        object_id + '> back to the UFO list?',
                    err_msg = '[modal-ufo] Wrong configuration, ex = ',
                    object = $scope._getIdentified(object_id),
                    object_sc_id = object.sc_identifier;

                if (confirm(ask_msg) === false) {
                    $log.warn('[modal-ufo] object kept identified.');
                    return;
                }

                satnetRPC.rCall(
                    'leop.ufo.forget',
                    [$rootScope.leop_id, object_id]
                ).then(
                    function (data) {
                        $log.info(
                            '[modal-ufo] <Object#' + data + '> back as a UFO.'
                        );
                        $scope._addUfo(object_id);
                        $scope._removeIdentified(object_id);
                        broadcaster.scRemoved(object_sc_id);
                    },
                    function (data) {
                        err_msg += JSON.stringify(data);
                        $log.warn(err_msg);
                        if (alert(err_msg) === false) {
                            $log.warn(err_msg);
                        }
                    }
                );
            };

            $scope.editCluster = function () {
                $scope.cluster.edit = true;
            };

            $scope.saveCluster = function () {

                var err_msg = '[modal-ufo] Wrong configuration, ex = ',
                    cfg = {
                        identifier: $rootScope.leop_id,
                        date: $scope.cluster.date,
                        tle_l1: $scope.cluster.tle_l1,
                        tle_l2: $scope.cluster.tle_l2
                    };

                satnetRPC.rCall('leop.setCfg', [$rootScope.leop_id, cfg])
                    .then(function (data) {
                        $log.info('[modal-ufo] New cluster cfg, id = ' + data);
                        $scope.cluster.edit = false;
                        $rootScope.$broadcast(CLUSTER_CFG_UPDATED_EV, cfg);
                        broadcaster.scUpdated($scope.cluster.sc_identifier);
                    }, function (data) {
                        err_msg += JSON.stringify(data);
                        $log.warn(err_msg);
                        if (alert(err_msg) === false) {
                            $log.warn(err_msg);
                        }
                    });

            };
            $scope.cancelCluster = function () {
                $scope.cluster.edit = false;
            };

            $scope.hide = function () { $modalInstance.close(); };
            $scope.init();

        }
    ]);