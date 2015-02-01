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

angular.module('logNotifierDirective', ['broadcaster'])
    .constant('TIMESTAMP_FORMAT', 'HH:mm:ss.sss')
    .controller('logNotifierCtrl', [
        '$scope', '$filter', 'broadcaster', 'TIMESTAMP_FORMAT',
        function ($scope, $filter, broadcaster, TIMESTAMP_FORMAT) {
            'use strict';

            $scope.eventLog = [];
            $scope.logEvent = function (event, message) {
                $scope.eventLog.unshift({
                    type: event.name,
                    timestamp: $filter('date')(new Date(), TIMESTAMP_FORMAT),
                    msg:  message
                });
            };

            $scope.$on('logEvent', function (event, message) {
                $scope.logEvent(event, message);
            });
            $scope.$on('infoEvent', function (event, message) {
                $scope.logEvent(event, message);
            });
            $scope.$on('warnEvent', function (event, message) {
                $scope.logEvent(event, message);
            });
            $scope.$on('errEvent', function (event, message) {
                $scope.logEvent(event, message);
            });
            $scope.$on('debEvent', function (event, message) {
                $scope.logEvent(event, message);
            });
            $scope.$on(broadcaster.KEEP_ALIVE_EVENT, function (event, message) {
                $scope.logEvent(event, 'KEEP ALIVE');
            });

        }
    ])
    .directive('logNotifier', function () {
        'use strict';

        return {
            restrict: 'E',
            templateUrl: 'templates/notifier/logNotifier.html'
        };

    });