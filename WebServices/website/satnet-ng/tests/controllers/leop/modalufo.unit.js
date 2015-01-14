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

var oArrays, xDicts;

module('modalufo.unit', {
    setup: function () {
        'use strict';
        oArrays = injector.get('oArrays');
        xDicts = injector.get('xDicts');
    }
});

test('objectArrayCheck tests', function () {
    'use strict';

    throws(
        function () {
            oArrays.check(null, '');
        },
        /is invalid/,
        "Null array, throws exception"
    );
    throws(
        function () {
            oArrays.check(undefined, '');
        },
        /is invalid/,
        "Null array, throws exception"
    );
    ok(oArrays.check([], ''), "Empty array, throws exception");
    throws(
        function () {
            oArrays.check([1], null);
        },
        /Wrong property/,
        "<null> property, throws exception"
    );
    throws(
        function () {
            oArrays.check([1], '');
        },
        /Wrong property/,
        "Wrong property, throws exception"
    );
    throws(
        function () {
            oArrays.check([1], 'aaa');
        },
        /Wrong property/,
        "Wrong property, throws exception"
    );

});
test('basic findMaxTuple tests', function () {
    'use strict';

    var input, actual;

    actual = oArrays.findMaxTuple([{ object_id: 1 }], 'object_id');
    deepEqual(actual, { index: 0, value: 1 }, 'Results differ');

    input = [
        {object_id: 4}, {object_id: 3}, {object_id: 5}, {object_id: -1}
    ];
    actual = oArrays.findMaxTuple(input, 'object_id');
    deepEqual(actual, { index: 2, value: 5 }, 'Results differ');

});

test('basic indexOf tests', function () {
    'use strict';

    var input;

    throws(
        function () {
            oArrays.indexOf([{ object_id: 1 }], 'object_id', 0);
        },
        /Pair not found/,
        "Pair not found, throws exception"
    );

    input = [
        {object_id: 4}, {object_id: 3}, {object_id: 5}, {object_id: -1}
    ];
    equal(oArrays.indexOf(input, 'object_id', 3), 1, 'Results differ');

});

test('basic split tests', function () {
    'use strict';

    throws(
        function () {
            oArrays.split(null, -1);
        },
        /is null/,
        'Array is null, an exception should have been thrown'
    );
    throws(
        function () {
            oArrays.split([], -1);
        },
        /columns should be/,
        'max_columns < 1, makes no sense!'
    );

    deepEqual(oArrays.split(undefined, 3), [], 'Results differ');
    deepEqual(oArrays.split([], 3), [], 'Results differ');
    deepEqual(oArrays.split([1, 2], 1), [[1], [2]], 'Results differ');
    deepEqual(
        oArrays.split([1, 2, 3, 4, 5, 6], 4),
        [[1, 2, 3, 4], [5, 6]],
        'Results differ'
    );

});

test('basic insert sorted', function () {
    'use strict';

    throws(
        function () {
            oArrays.insertSorted([{'object_id': 1}], 'object_id', null);
        },
        /is null/,
        'Element is null, an exception should have been thrown'
    );
    throws(
        function () {
            oArrays.insertSorted([{'object_id': 1}], 'object_id', {});
        },
        /Invalid element/,
        'Element is empty, an exception should have been thrown'
    );
    throws(
        function () {
            oArrays.insertSorted([], 'object_id', {});
        },
        /Invalid element/,
        'Element is empty, an exception should have been thrown'
    );

    deepEqual(
        oArrays.insertSorted([], 'object_id', {'object_id': 2}),
        [{'object_id': 2}],
        'Array should contain a new element'
    );
    deepEqual(
        oArrays.insertSorted(
            [{'object_id': 1}],
            'object_id',
            {'object_id': 2}
        ),
        [{'object_id': 1}, {'object_id': 2}],
        'Array should contain a two elements'
    );

    deepEqual(
        oArrays.insertSorted(
            [{'object_id': 3}],
            'object_id',
            {'object_id': 2}
        ),
        [{'object_id': 2}, {'object_id': 3}],
        'Array should contain a two elements'
    );

    deepEqual(
        oArrays.insertSorted(
            [{'object_id': 3}, {'object_id': 5}, {'object_id': 7}],
            'object_id',
            {'object_id': 2}
        ),
        [
            {'object_id': 2},
            {'object_id': 3},
            {'object_id': 5},
            {'object_id': 7}
        ],
        'Array should contain a two elements'
    );

});

test('basic array2dict tests', function () {
    'use strict';

    throws(
        function () {
            oArrays.array2dict([], null);
        },
        /is null/,
        'Property is null, an exception should have been thrown'
    );

    deepEqual(oArrays.array2dict([], 'object_id'), {}, 'Results differ');
    deepEqual(
        oArrays.array2dict([{'object_id': 1}], 'object_id'),
        {1: {'object_id': 1}},
        'Results differ'
    );
    deepEqual(
        oArrays.array2dict(
            [{'object_id': 1}, {'object_id': 2}],
            'object_id'
        ),
        {1: {'object_id': 1}, 2: {'object_id': 2}},
        'Results differ'
    );

});

test('basic xDicts.check() tests', function () {
    'use strict';

    throws(
        function () {
            xDicts.check(null, null);
        },
        /is invalid/,
        'dict is null, an exception should have been thrown'
    );
    throws(
        function () {
            xDicts.check(undefined, null);
        },
        /is invalid/,
        'dict is undefined, an exception should have been thrown'
    );
    throws(
        function () {
            xDicts.check({}, null);
        },
        /is invalid/,
        'dict is undefined, an exception should have been thrown'
    );
    throws(
        function () {
            xDicts.check({a: 'a'}, null);
        },
        /is invalid/,
        'dict is undefined, an exception should have been thrown'
    );
    throws(
        function () {
            xDicts.check({a: 'a'}, undefined);
        },
        /is invalid/,
        'dict is undefined, an exception should have been thrown'
    );

});

test('basic xDicts.findMaxTuple() tests', function () {
    'use strict';

    deepEqual(
        xDicts.findMaxTuple({}, 'object_id'),
        [undefined, 0],
        'Should return an empty result'
    );
    deepEqual(
        xDicts.findMaxTuple({1: {object_id: 2}}, 'object_id'),
        ['1', 2],
        'Should return an empty result'
    );
    deepEqual(
        xDicts.findMaxTuple(
            {1: {object_id: 2}, 2: {object_id: 2}},
            'object_id'
        ),
        ['2', 2],
        'Should return an empty result'
    );
    deepEqual(
        xDicts.findMaxTuple(
            {3: {object_id: 3}, 1: {object_id: 1}, 2: {object_id: 2}},
            'object_id'
        ),
        ['3', 3],
        'Should return an empty result'
    );
    deepEqual(
        xDicts.findMaxTuple(
            {3: {object_id: 4}, 5: {object_id: 5}, 2: {object_id: 2}},
            'object_id'
        ),
        ['5', 5],
        'Should return an empty result'
    );

});

test('basic xDicts.isEmpty() tests', function () {
    'use strict';

    ok(xDicts.isEmpty({}), 'Should be empty');
    ok(!xDicts.isEmpty({a: 'b'}), 'Should NOT be empty');

});