/*
   Copyright 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

angular.module('countdownDirective', [ 'satnet-services' ])
    .constant('COUNTDOWN_END_EV', 'launch-countdown-end')
    .controller('countdownCtrl', [
        '$rootScope', '$scope', '$timeout', 'satnetRPC',
        function ($rootScope, $scope, $timeout, satnetRPC) {
            'use strict';

            $scope._timer = {};
            $scope._counter = 0;
            $scope.datems = 0;
            $scope.label = 'Time to launch';

            $scope.beat = function () {
                $scope._timer = $timeout(function () {
                    console.log($scope._counter);
                    $scope._counter -= 1;
                    $scope.datems = $scope._counter * 1000;
                    if ($scope._counter === 0) {
                        $rootScope.$broadcast('launch-countdown-end');
                        $timeout.cancel($scope._timer);
                    } else {
                        $scope.beat();
                    }
                }, 1000);
            };

            $scope.init = function () {

                satnetRPC.rCall('leop.cfg', [$rootScope.leop_id]).then(
                    function (data) {
                        var launch = moment(data.date),
                            now = moment(),
                            diff = moment.duration(launch.diff(now));
                        $scope._counter = diff;
                        $scope.beat();
                    }
                );

            };

            $scope.init();

        }
    ])
    .directive('countdown', function () {
        'use strict';

        return {
            restrict: 'E',
            templateUrl: 'templates/countdown/countdown.html'
        };

    });