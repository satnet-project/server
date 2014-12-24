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

var TIMESTAMP_FORMAT = 'HH:mm:ss.sss';

////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////// Main Application Module
////////////////////////////////////////////////////////////////////////////////

var app = angular.module('satnet-ui', [
    // AngularJS libraries
    'leaflet-directive',
    'ngResource', 'ngCookies',
    'remoteValidation', 'jsonrpc',
    // level 1 services/models
    'common', 'map-services',
    'celestrak-services', 'satnet-services', 'broadcaster',
    'x-satnet-services',
    // level 2 services/models
    'marker-models',
    'groundstation-models',
    'spacecraft-models',
    // level 3 services/models
    'x-groundstation-models',
    'x-server-models',
    'x-spacecraft-models',
    // level 4 (controllers),
    'ui-map-controllers',
    'ui-menu-controllers',
    'ui-leop-menu-controllers',
    'ui-leop-modalsc-controllers',
    'ui-leop-modalgs-controllers'
]);

// level 1 services
angular.module('common');
angular.module('map-services');
angular.module('celestrak-services');
angular.module('satnet-services');
angular.module('x-satnet-services');
angular.module('broadcaster');
// level 2 services
angular.module('marker-models');
angular.module('groundstation-models');
angular.module('spacecraft-models');
// level 3 services
angular.module('x-groundstation-models');
angular.module('x-spacecraft-models');
// level 4 controllers
angular.module('ui-map-controllers');
angular.module('ui-menu-controllers');
angular.module('ui-leop-menu-controllers');
angular.module('ui-leop-modalsc-controllers');
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
                //$delegate.error.apply(null, ['[error] ' + args]);
                $delegate.error.apply(null, arguments);
                //Logging.error.apply(null,arguments)
                //rScope.$broadcast('errEvent', arguments);
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
    '$rootScope', '$window', '$log', '$http', '$cookies',
    function ($rootScope, $window, $log, $http, $cookies) {
        'use strict';
        $rootScope.leop_id = $window.leop_id;
        console.log('>> $rootScope.leop_id = ' + $rootScope.leop_id);
        console.log('>> $window.leop_id = ' + $window.leop_id);
        $log.setScope($rootScope);
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    }
]);

app.controller('NotificationAreaController', [
    '$scope', '$filter',
    function ($scope, $filter) {
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