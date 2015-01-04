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

/**
 * Main application for the norminal operational phase.
 * @type {ng.IModule}
 */
var app = angular.module('satnet-ui', [
    // AngularJS libraries
    'jsonrpc',
    'ngCookies',
    'ngResource',
    'leaflet-directive',
    'remoteValidation',
    // level 1 services/models
    'broadcaster',
    'map-services',
    'celestrak-services',
    'satnet-services',
    'x-satnet-services',
    // level 2 services/models
    'marker-models',
    // level 3 services/models
    'x-server-models',
    'x-spacecraft-models',
    'x-groundstation-models',
    // level 4 (controllers),
    'ui-map-controllers',
    'ui-menu-controllers',
    'ui-modalsc-controllers',
    'ui-modalgs-controllers'
]);

// level 1 services
angular.module('broadcaster');
angular.module('map-services');
angular.module('satnet-services');
angular.module('x-satnet-services');
angular.module('celestrak-services');
// level 2 services
angular.module('marker-models');
// level 3 services
angular.module('x-server-models');
angular.module('x-spacecraft-models');
angular.module('x-groundstation-models');
// level 4 controllers
angular.module('ui-map-controllers');
angular.module('ui-menu-controllers');
angular.module('ui-modalsc-controllers');
angular.module('ui-modalgs-controllers');

/**
 * Configuration of the main AngularJS logger so that it broadcasts all logging
 * messages as events that can be catched by other visualization UI controllers.
 */
app.config(function ($provide) {
    'use strict';
    $provide.decorator('$log', function ($delegate) {
        var rScope = null;
        return {
            setScope: function (scope) { rScope = scope; },
            log: function (args) {
                console.log('@log event');
                $delegate.log.apply(null, ['[log] ' + args]);
                rScope.$broadcast('logEvent', args);
            },
            info: function (args) {
                console.log('@info event');
                $delegate.info.apply(null, ['[info] ' + args]);
                rScope.$broadcast('infoEvent', args);
            },
            error: function () {
                console.log('@error event');
                //$delegate.error.apply(null, ['[error] ' + args]);
                $delegate.error.apply(null, arguments);
                //Logging.error.apply(null,arguments)
                rScope.$broadcast('errEvent', arguments);
            },
            warn: function (args) {
                console.log('@warn event');
                $delegate.warn.apply(null, ['[warn] ' + args]);
                rScope.$broadcast('warnEvent', args);
            },
            debug: function (args) {
                console.log('@debug event');
                rScope.$broadcast('debugEvent', args);
            },
        };
    });
});

/**
 * Main run method for the AngularJS app.
 */
app.run([
    '$rootScope', '$log', '$http', '$cookies',
    function ($rootScope, $log, $http, $cookies) {
        'use strict';
        $log.setScope($rootScope);
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    }
]);

app.constant('TIMESTAMP_FORMAT', 'HH:mm:ss.sss')
    .controller('NotificationAreaController', [
        '$scope', '$filter', 'TIMESTAMP_FORMAT',
        function ($scope, $filter, TIMESTAMP_FORMAT) {

            'use strict';
            $scope.eventLog = [];
            $scope.logEvent = function (event, message) {
                $scope.eventLog.unshift({
                    'type': event.name,
                    'timestamp': $filter('date')(new Date(), TIMESTAMP_FORMAT),
                    'msg':  message
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

        }
    ]);