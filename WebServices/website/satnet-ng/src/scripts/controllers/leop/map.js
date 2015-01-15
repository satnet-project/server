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
    'ui-leop-map-controllers',
    [
        'satnetRPC',
        'marker-models',
        'x-spacecraft-models',
        'x-server-models',
        'x-groundstation-models'
    ]
);

angular.module('ui-leop-map-controllers')
    .controller('LEOPMapController', [
        '$rootScope', '$scope', '$log', 'markers', 'xsc', 'xserver', 'xgs',
        function ($rootScope, $scope, $log, markers, xsc, xserver, xgs) {

            'use strict';

            markers.configureMapScope($scope);
            xsc.initListeners();
            xgs.initListeners();

            xsc.initAllLEOP().then(function (spacecraft) {
                $log.log(
                    '[map-controller] Spacecraft =' + JSON.stringify(spacecraft)
                );
            });
            xserver.initStandalone().then(function (server) {
                $log.log(
                    '[map-controller] Server =' + JSON.stringify(server)
                );
                xgs.initAllLEOP($rootScope.leop_id).then(function (gss) {
                    $log.log(
                        '[map-controller] Ground Station(s) = ' +
                            JSON.stringify(gss)
                    );
                });
            });

        }
    ]);
