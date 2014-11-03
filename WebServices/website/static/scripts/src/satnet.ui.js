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
    // level 1 services
    'common', 'map-services',
    'celestrak-services', 'satnet-services', 'broadcaster',
    // level 2 services
    'groundstation-models', 'simulator',
    // level 3 services
    'x-groundstation-models',
    // level 4 (controllers),
    'ui-map-controllers', 'ui-modalsc-controllers', 'ui-modalgs-controllers'
]);

// level 1 services
angular.module('common');
angular.module('map-services');
angular.module('celestrak-services');
angular.module('satnet-services');
angular.module('broadcaster');
// level 2 services
angular.module('groundstation-models');
angular.module('simulator');
// level 3 services
angular.module('x-groundstation-models');
// level 4 controllers
angular.module('ui-map-controllers');
angular.module('ui-modalsc-controllers');
angular.module('ui-modalgs-controllers');

/**
 * Configuration of the main AngularJS logger so that it broadcasts all logging
 * messages as events that can be catched by other visualization UI controllers.
 */
app.config(function($provide) {
    'use strict';
    
    $provide.decorator('$log', function($delegate) {
        var rScope = null;
        return  {
            setScope: function(scope) { rScope = scope; },
            log: function () {
                $delegate.log.apply(null, ['[log] ' + arguments[0]]);
                rScope.$broadcast('logEvent', arguments[0]);
            },
            info: function () {
                $delegate.info.apply(null, ['[info] ' + arguments[0]]);
                rScope.$broadcast('infoEvent', arguments[0]);
            },
            error: function () {
                $delegate.error.apply(null, ['[error] ' + arguments[0]]);
                rScope.$broadcast('errEvent', arguments[0]);
            },
            warn: function () {
                $delegate.warn.apply(null, ['[warn] ' + arguments[0]]);
                rScope.$broadcast('warnEvent', arguments[0]);
            }
        };
    });
});

/**
 * Main run method for the AngularJS app.
 */
app.run([
    '$rootScope', '$log', '$http', '$cookies',
    function($rootScope, $log, $http, $cookies) {
        
        'use strict';
        
        $log.setScope($rootScope);
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        
    }
]);

app.controller('NotificationAreaController', [
    '$scope', '$filter', function($scope, $filter) {

    'use strict';
        
    $scope.eventLog = [];
    $scope._logEvent = function (event, message) {
        $scope.eventLog.unshift({
            'type': event.name,
            'timestamp': $filter('date')(new Date(), TIMESTAMP_FORMAT),
            'msg':  message
        });
    };

    $scope.$on('logEvent', function(event, message) {
        $scope._logEvent(event, message);
    });
    $scope.$on('infoEvent', function(event, message) {
        $scope._logEvent(event, message);
    });
    $scope.$on('warnEvent', function(event, message) {
        $scope._logEvent(event, message);
    });
    $scope.$on('errEvent', function(event, message) {
        $scope._logEvent(event, message);
    });

}]);