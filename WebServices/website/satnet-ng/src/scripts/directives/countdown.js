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
        '$rootScope', '$log', '$scope', '$timeout', 'satnetRPC',
        function ($rootScope, $log, $scope, $timeout, satnetRPC) {
            'use strict';

            $scope.cd = {
                label: 'EXPIRED',
                diff: '',
                expired: false,
                hide: false,
                _launch: {},
                _diff: {},
                _timer: {}
            };

            $scope._endBeat = function () {
                $rootScope.$broadcast('launch-countdown-end');
                $timeout.cancel($scope._timer);
                $scope.cd.expired = true;
            };

            $scope.toggle = function () {
                $scope.cd.hide = !$scope.cd.hide;
            };

            $scope.beat = function () {
                $scope.cd._timer = $timeout(function () {

                    var now = moment().utc();

                    if (($scope.cd._launch.isBefore(now) === true) ||
                            ($scope.cd._launch.isSame(now) === true)) {
                        $scope._endBeat();
                        return;
                    }

                    $scope.cd._diff = moment.duration(
                        $scope.cd._launch.diff(now)
                    );
                    $scope.cd.diff = $scope.cd._diff.toISOString();
                    $scope.beat();

                }, 990);
            };

            $scope._init = function (cfg) {
                var now = moment().utc();
                $scope.cd._launch = moment(cfg.date);
                $scope.cd._diff = moment.duration($scope.cd._launch.diff(now));
                $scope.beat();
            };

            $scope.init = function () {
                satnetRPC.rCall('leop.cfg', [$rootScope.leop_id]).then(
                    function (cfg) { $scope._init(cfg); }
                );
                $scope.$on('cluster-cfg-updated', function (id, cfg) {
                    console.log('EVENT, id = ' + id);
                    $log.info('@countdown: updating cluster, cfg = ' + cfg);
                    $scope._init(cfg);
                });
            };

            $scope.init();

        }
    ])
    .filter('cdDate', function () {
        'use strict';

        return function (input) {

            return input.replace(/P/, '').replace(/S/, '')
                        .replace(/DT/, ' days ').replace(/H/, ':').replace(/M/, ':')
                        .replace(/\.[0-9]{1,}/, '');

        };

    })
    .directive('countdown', function () {
        'use strict';

        return {
            restrict: 'E',
            templateUrl: 'templates/countdown/countdown.html'
        };

    });