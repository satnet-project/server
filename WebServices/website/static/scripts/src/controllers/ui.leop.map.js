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
        'leaflet-directive',
        'broadcaster',
        'map-services',
        'marker-models',
        'groundstation-models',
        'x-groundstation-models',
        'spacecraft-models',
        'x-spacecraft-models',
        'x-server-models'
    ]
);

angular.module('ui-map-controllers')
    .constant('LAT', 32.630)
    .constant('LNG', 8.933)
    .constant('D_ZOOM', 10)
    .constant('GS_ELEVATION', 15.0)
    .controller('MapController', [
        '$scope',
        '$log',
        'broadcaster',
        'maps',
        'markers',
        'gs',
        'xgs',
        'sc',
        'xsc',
        'xserver',
        'LAT',
        'LNG',
        'ZOOM',
        function (
            $scope,
            $log,
            broadcaster,
            maps,
            markers,
            gs,
            xgs,
            sc,
            xsc,
            xserver,
            LAT,
            LNG,
            ZOOM
        ) {

            'use strict';

            angular.extend($scope, {
                center: { lat: LAT, lng: LNG, zoom: ZOOM },
                layers: {
                    baselayers: {
                        esri_baselayer: {
                            name: 'ESRI Base Layer',
                            type: 'xyz',
                            url: 'http://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',
                            layerOptions: {
                                attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ'
                            }
                        },
                        osm_baselayer: {
                            name: 'OSM Base Layer',
                            type: 'xyz',
                            url: 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                            layerOptions: {
                                attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                            }
                        }
                    },
                    overlays: {}
                },
                markers: []
            });

            maps.createMainMap(true).then(function (data) {
                $log.log('[map-controller] <' + maps.asString(data) + '>');
            });

            xserver.initStandalone().then(function (server) {
                $log.log(
                    '[map-controller] Server {'
                        + '    identifier: ' + server.id
                        + '    latitude: ' + server.latitude
                        + '    longitude: ' + server.longitude
                        + '}'
                );
                xgs.initAllLEOP().then(function (gss) {
                    $log.log(
                        '[map-controller] Ground Stations = '
                            + gs.gssAsString(gss)
                    );
                });
            });

            $scope.layers.overlays = angular.extend(
                {},
                maps.getNgOverlays(),
                markers.getNgOverlays()
            );

            $scope.$on(broadcaster.GS_ADDED_EVENT, function (event, gsId) {
                console.log(
                    '@on-gs-added-event, event = ' + event + 'gsId = ' + gsId
                );
                xgs.addGS(gsId);
            });
            $scope.$on(broadcaster.GS_REMOVED_EVENT, function (event, gsId) {
                console.log(
                    '@on-gs-removed-event, event = ' + event + 'gsId = ' + gsId
                );
                gs.remove(gsId);
            });
            $scope.$on(broadcaster.GS_UPDATED_EVENT, function (event, gsId) {
                console.log(
                    '@on-gs-updated-event, event = ' + event + 'gsId = ' + gsId
                );
                xgs.updateGS(gsId);
            });

            $scope.$on(broadcaster.SC_ADDED_EVENT, function (event, scId) {
                console.log(
                    '@on-sc-added-event, event = ' + event + 'scId = ' + scId
                );
                xsc.addSC(scId);
            });
            $scope.$on(broadcaster.SC_REMOVED_EVENT, function (event, scId) {
                console.log(
                    '@on-sc-removed-event, event = ' + event + 'scId = ' + scId
                );
                sc.remove(scId);
            });
            $scope.$on(broadcaster.SC_UPDATED_EVENT, function (event, scId) {
                console.log(
                    '@on-sc-updated-event, event = ' + event + 'scId = ' + scId
                );
                console.log('NOT YET IMPLEMENTED!');
                xsc.updateSC(scId);
            });

        }
    ]);