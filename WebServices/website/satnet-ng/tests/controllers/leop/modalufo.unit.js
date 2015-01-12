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
 * Created by rtubio on 10/1/14.
 */

var injector = angular.injector([
    'ngMock', 'ng', 'ui-leop-modalufo-controllers'
]);

var objectArrays;

module('modalufo.unit', {
    setup: function () {
        'use strict';
        objectArrays = injector.get('objectArrays');
    }
});

test('objectArrayCheck tests', function () {
    'use strict';

    throws(
        function () {
            objectArrays.check(null, '');
        },
        /is null/,
        "Null array, throws exception"
    );
    ok(objectArrays.check([], ''), "Empty array, throws exception");
    throws(
        function () {
            objectArrays.check([1], null);
        },
        /Wrong property/,
        "<null> property, throws exception"
    );
    throws(
        function () {
            objectArrays.check([1], '');
        },
        /Wrong property/,
        "Wrong property, throws exception"
    );
    throws(
        function () {
            objectArrays.check([1], 'aaa');
        },
        /Wrong property/,
        "Wrong property, throws exception"
    );

});
test('basic findMaxTuple tests', function () {
    'use strict';

    var input, actual;

    actual = objectArrays.findMaxTuple([{ object_id: 1 }], 'object_id');
    deepEqual(actual, { index: 0, value: 1 }, 'Results differ');

    input = [
        {object_id: 4}, {object_id: 3}, {object_id: 5}, {object_id: -1}
    ];
    actual = objectArrays.findMaxTuple(input, 'object_id');
    deepEqual(actual, { index: 2, value: 5 }, 'Results differ');

});

test('basic indexOf tests', function () {
    'use strict';

    var input;

    throws(
        function () {
            objectArrays.indexOf([{ object_id: 1 }], 'object_id', 0);
        },
        /Pair not found/,
        "Pair not found, throws exception"
    );

    input = [
        {object_id: 4}, {object_id: 3}, {object_id: 5}, {object_id: -1}
    ];
    equal(objectArrays.indexOf(input, 'object_id', 3), 1, 'Results differ');

});

test('basic split tests', function () {
    'use strict';

    throws(
        function () {
            objectArrays.split(null, -1);
        },
        /is null/,
        'Array is null, an exception should have been thrown'
    );
    throws(
        function () {
            objectArrays.split([], -1);
        },
        /columns should be/,
        'max_columns < 1, makes no sense!'
    );

    deepEqual(objectArrays.split(undefined, 3), [], 'Results differ');
    deepEqual(objectArrays.split([], 3), [], 'Results differ');
    deepEqual(objectArrays.split([1, 2], 1), [[1], [2]], 'Results differ');
    deepEqual(
        objectArrays.split([1, 2, 3, 4, 5, 6], 4),
        [[1, 2, 3, 4], [5, 6]],
        'Results differ'
    );

});