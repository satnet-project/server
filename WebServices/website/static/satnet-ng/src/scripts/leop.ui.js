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
 * Main application for the LEOP operational phase.
 * @type {ng.IModule}
 */
var app = angular.module('leop-ui', [
    // AngularJS libraries
    'jsonrpc',
    'ngCookies',
    'ngResource',
    'leaflet-directive',
    'remoteValidation',
    // level 1 services
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
    'ui-leop-map-controllers',
    'ui-menu-controllers',
    'ui-leop-menu-controllers',
    'ui-leop-modalufo-controllers',
    'ui-leop-modalgs-controllers'
]);

// level 1 services
angular.module('broadcaster');
angular.module('map-services');
angular.module('celestrak-services');
angular.module('satnet-services');
angular.module('x-satnet-services');
// level 2 services (bussiness logic layer)
angular.module('marker-models');
// level 3 services
angular.module('x-server-models');
angular.module('x-spacecraft-models');
angular.module('x-groundstation-models');
// level 4 controllers
angular.module('ui-leop-map-controllers');
angular.module('ui-menu-controllers');
angular.module('ui-leop-menu-controllers');
angular.module('ui-leop-modalufo-controllers');
angular.module('ui-leop-modalgs-controllers');

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
                $delegate.log.apply(null, ['[log] ' + args]);
                rScope.$broadcast('logEvent', args);
            },
            info: function (args) {
                $delegate.info.apply(null, ['[info] ' + args]);
                rScope.$broadcast('infoEvent', args);
            },
            error: function () {
                $delegate.error.apply(null, arguments);
            },
            warn: function (args) {
                $delegate.warn.apply(null, ['[warn] ' + args]);
                rScope.$broadcast('warnEvent', args);
            }
        };
    });
});

/**
 * Main run method for the AngularJS app.
 */
app.run([
    '$rootScope', '$log', '$http', '$cookies', '$window',
    function ($rootScope, $log, $http, $cookies, $window) {
        'use strict';
        $log.setScope($rootScope);
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        $rootScope.leop_id = $window.leop_id;
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