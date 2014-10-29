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
    'simulator', [
        'celestrak-services'
    ]
);

angular.module('simulator')
    .service('simulator', [ 'celestrak', function(celestrak) {

        this.estimateTrack = function (scTleId) {
            return celestrak.findTle(scTleId).then(function(data) {
                console.log('> scTleId = ' + scTleId);
                var sc = satellite.twoline2satrec(
                    data['line_1'], data['line_2']
                );
                console.log(
                    '> l1 = ' + data['line_1'] + ', l2 = ' + data['line_2']
                );
            });
        };

    }
]);