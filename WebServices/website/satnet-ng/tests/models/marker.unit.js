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
    'ngMock', 'ng', 'marker-models'
]);
var markerModels;

module('marker.unit', {
    setup: function () {
        'use strict';
        markerModels = serviceLocator.get('markers');
    }
});

    /*
    console.log(
        '>>> groundtrack = ' +
            JSON.stringify(groundtrack)
                .replace(/\[/g, '[\n')
                .replace(/\]/g, '\n]')
                .replace(/\}\,/g, '},\n')
                .replace(/\{/g, '    {')
    );
    */
    /*
    console.log(
        '### result = ' +
            JSON.stringify(_result)
                .replace(/"durations/, '\n\t"durations')
                .replace(/"positions/, '\n\t"positions')
                .replace(/"geopoints/, '\n\t"geopoints')
    );
    */

test('basic readTrackOptimized tests', function () {
    'use strict';

    var groundtrack = [],
        nowUs = Date.now() * 1000,
        tomorrowUs = moment().add(1, "days").toDate().getTime() * 1000;

    throws(
        function () {
            markerModels.readTrack(null);
        },
        /is empty/,
        "Empty groundtrack array, throws exception"
    );
    throws(
        function () {
            markerModels.readTrack(groundtrack);
        },
        /is empty/,
        "Empty groundtrack array, throws exception"
    );

    groundtrack = [
        { timestamp: nowUs - 10000, latitude: 12.00, longitude: 145.00 }
    ];
    /*
    console.log(
        '>>> groundtrack = ' +
            JSON.stringify(groundtrack)
                .replace(/\[/g, '[\n')
                .replace(/\]/g, '\n]')
                .replace(/\}\,/g, '},\n')
                .replace(/\{/g, '    {')
    );
    */
    throws(
        function () {
            markerModels.readTrack(groundtrack);
        },
        /No valid points/,
        "No valid points, throws exception"
    );

    groundtrack = [ { timestamp: 0, latitude: 11.00, longitude: 144.00 } ];
    throws(
        function () { markerModels.readTrack(groundtrack); },
        /No valid points/,
        "No valid points, throws exception"
    );

    groundtrack = [
        { timestamp: tomorrowUs + 1000000, latitude: 12.00, longitude: 145.00 }
    ];
    /*
    console.log(
        '>>> groundtrack = ' +
            JSON.stringify(groundtrack)
                .replace(/\[/g, '[\n')
                .replace(/\]/g, '\n]')
                .replace(/\}\,/g, '},\n')
                .replace(/\{/g, '    {')
    );
    */
    throws(
        function () { markerModels.readTrack(groundtrack); },
        /No valid points/,
        "No valid points, throws exception"
    );

});

test('extended readTrackOptimized tests', function () {
    'use strict';

    var _result, groundtrack = [],
        nowUs = Date.now() * 1000;

    groundtrack.push(
        { timestamp:  nowUs - 10000, latitude: 12.00, longitude: 145.00 }
    );
    throws(
        function () { markerModels.readTrack(groundtrack); },
        /No valid points/,
        "No valid points, throws exception"
    );

    groundtrack.push(
        { timestamp:  nowUs - 100000, latitude: 13.00, longitude: 146.00 }
    );
    throws(
        function () {
            markerModels.readTrack(groundtrack);
        },
        /No valid points/,
        "No valid points, throws exception"
    );

    groundtrack.push(
        { timestamp: nowUs + 40000000000, latitude: 14.00, longitude: 147.00 }
    );
    throws(
        function () {
            markerModels.readTrack(groundtrack);
        },
        /No valid points/,
        "No valid points, throws exception"
    );

    groundtrack.push(
        { timestamp: nowUs + 50000000000, latitude: 15.00, longitude: 148.00 }
    );
    _result = markerModels.readTrack(groundtrack);
    deepEqual(_result.durations, [10000000]);
    deepEqual(_result.positions, [[14, 147], [15, 148]]);

    groundtrack.push(
        { timestamp: nowUs + 400000000000, latitude: 16.00, longitude: 149.00 }
    );
    _result = markerModels.readTrack(groundtrack);
    deepEqual(_result.durations, [10000000]);
    deepEqual(_result.positions, [[14, 147], [15, 148]]);

});