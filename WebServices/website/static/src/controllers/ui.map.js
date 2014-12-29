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
    'ui-map-controllers',
    [
        'marker-models',
        'x-groundstation-models',
        'x-spacecraft-models',
        'x-server-models'
    ]
);

angular.module('ui-map-controllers')
    .controller('MapController', [
        '$scope', '$log', 'markers', 'xgs', 'xsc', 'xserver',
        function ($scope, $log, markers, xgs, xsc, xserver) {

            'use strict';

            markers.configureMapScope($scope);
            xsc.initListeners();
            xgs.initListeners();

            xsc.initAll().then(function (spacecraft) {
                $log.log(
                    '[map-controller] Spacecraft =' + JSON.stringify(spacecraft)
                );
            });
            xserver.initStandalone().then(function (server) {
                $log.log(
                    '[map-controller] Server =' + JSON.stringify(server)
                );
                xgs.initAll().then(function (gs_markers) {
                    $log.log(
                        '[map-controller] Ground Station(s) = ' +
                            JSON.stringify(gs_markers)
                    );
                });
            });

        }
    ]);