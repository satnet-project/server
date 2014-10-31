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
    'ui-map-controllers', [
        'leaflet-directive',
        'broadcaster', 'maps',
        'groundstation-models', 'x-groundstation-models',
        'spacecraft-models',
        'ui-modalsc-controllers'
    ]
);

angular.module('ui-map-controllers').controller('MapController', [
    '$scope', '$log',
    'leafletData', 'broadcaster', 'gs', 'xgs', 'sc', 'maps',
    function(
        $scope, $log,
        leafletData, broadcaster, gs, xgs, sc, maps
    ) {
        
        'use strict';
        
        $scope.markers = [];
        angular.extend($scope, {
            center: {
                lat: maps.DEFAULT_LAT,
                lng: maps.DEFAULT_LNG,
                zoom: maps.DEFAULT_ZOOM
            },
            defaults: { worldCopyJump: true }
        });
        leafletData.getMap().then(function(map) {
            maps.locateUser($log, map, null);
            L.terminator({ fillOpacity: 0.125 }).addTo(map);
            xgs.initGSMarkers();
            sc.init().then(function(data) {
                console.log('^^^^^ data = ' + JSON.stringify(data));
            });
        });
        $scope.$on(broadcaster.GS_ADDED_EVENT, function(event, gsId) {
            xgs.addGSMarker(gsId);
        });
        $scope.$on(broadcaster.GS_REMOVED_EVENT, function(event, gsId) {
            gs.remove(gsId);
        });
        $scope.$on(broadcaster.GS_UPDATED_EVENT, function(event, gsId) {
            xgs.updateGSMarker(gsId);
        });
    }
]);

angular.module('ui-map-controllers').controller('GSMenuCtrl', [
    '$scope', '$log', '$modal', 'satnetRPC',
    function($scope, $log, $modal, satnetRPC) {
        
        'use strict';
        
        $scope.gsIds = [];
        $scope.addGroundStation = function() {
            var modalInstance = $modal.open({
                templateUrl: '/static/scripts/src/templates/addGroundStation.html',
                controller: 'AddGSModalCtrl',
                backdrop: 'static'
            });
        };
        $scope.editGroundStation = function(g) {
            var modalInstance = $modal.open({
                templateUrl: '/static/scripts/src/templates/editGroundStation.html',
                controller: 'EditGSModalCtrl', backdrop: 'static',
                resolve: { groundstationId: function() { return(g); } }
            });
        };
        $scope.refreshGSList = function() {
            satnetRPC.call('gs.list', [], function(data) {
                $scope.gsIds = data.slice(0);
            });
        };
        $scope.refreshGSList();
    }
]);

angular.module('ui-map-controllers').controller('SCMenuCtrl',
    [ '$scope', '$log', '$modal', 'satnetRPC',
    function($scope, $log, $modal, satnetRPC) {
        
        'use strict';
        
        $scope.scIds = [];
        $scope.addSpacecraft = function() {
            var modalInstance = $modal.open({
                templateUrl: '/static/scripts/src/templates/addSpacecraft.html',
                controller: 'AddSCModalCtrl', backdrop: 'static'
            });
        };
        $scope.editSpacecraft = function(s) {
            var modalInstance = $modal.open({
                templateUrl: '/static/scripts/src/templates/editSpacecraft.html',
                controller: 'EditSCModalCtrl', backdrop: 'static',
                resolve: { spacecraftId: function() { return(s); } }
            });
        };
        $scope.refreshSCList = function() {
            satnetRPC.call('sc.list', [], function(data) {
                $scope.scIds = data.slice(0);
            });
        };
        $scope.refreshSCList();
    }
]);

angular.module('ui-map-controllers').controller('ExitMenuCtrl', [
    '$scope', '$log',
    function($scope, $log) {
        
        'use strict';
        
        $scope.home = function () { $log.info('Exiting...'); };
        
    }
]);