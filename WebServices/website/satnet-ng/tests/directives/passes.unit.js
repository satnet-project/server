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

var serviceLocator = angular.injector([
    'ngMock', 'ng', 'passDirective'
]);
var passSlotsService;

module('marker.unit', {
    setup: function () {
        'use strict';
        passSlotsService = serviceLocator.get('passSlotsService');
    }
});

test('basic _parseSlots tests', function () {
    'use strict';

    throws(
        function () {
            passSlotsService._parseSlots(null);
        },
        /is null/,
        "Null slot array, throws exception"
    );

    deepEqual(
        passSlotsService._parseSlots([]),
        [],
        'Should have returned an empty array'
    );

    // 1) basic simple slot
    var actual,
        input = [{
            gs_identifier: 'my-gs-1',
            sc_identifier: 'my-sc-1',
            slot_start: '2002-12-25T00:00:00-06:39',
            slot_end: '2002-12-25T01:00:00-06:39'
        }],
        expected = [{
            name: 'my-gs-1',
            tasks: [{
                name: 'my-sc-1',
                from: new Date('2002-12-25T00:00:00-06:39'),
                to: new Date('2002-12-25T01:00:00-06:39')
            }]
        }];

    actual = passSlotsService._parseSlots(input);
    deepEqual(actual, expected, 'Should have returned a different result');

    // 2) basic simple slot
    input.push({
        gs_identifier: 'my-gs-1',
        sc_identifier: 'my-sc-1',
        slot_start: '2002-12-26T00:00:00-06:39',
        slot_end: '2002-12-26T01:00:00-06:39'
    });
    expected[0].tasks.push({
        name: 'my-sc-1',
        from: new Date('2002-12-26T00:00:00-06:39'),
        to: new Date('2002-12-26T01:00:00-06:39')
    });
    actual = passSlotsService._parseSlots(input);

    deepEqual(actual, expected, 'Should have returned a different result');

    // 3) basic simple slot
    input.push({
        gs_identifier: 'my-gs-2',
        sc_identifier: 'my-sc-1',
        slot_start: '2002-12-27T00:00:00-06:39',
        slot_end: '2002-12-27T01:00:00-06:39'
    });
    expected.push({
        name: 'my-gs-2',
        tasks: [{
            name: 'my-sc-1',
            from: new Date('2002-12-27T00:00:00-06:39'),
            to: new Date('2002-12-27T01:00:00-06:39')
        }]
    });
    actual = passSlotsService._parseSlots(input);

    deepEqual(actual, expected, 'Should have returned a different result');

});