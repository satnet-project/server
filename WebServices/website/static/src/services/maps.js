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
 * Created by rtubio on 11/01/14.
 */

/** Module definition (empty array is vital!). */
angular.module('map-services', [
    'leaflet-directive',
    'satnet-services'
]);

angular.module('map-services')
    .constant('T_OPACITY', 0.125)
    .constant('LAT', 37.7833)
    .constant('LNG', -122.4167)
    .constant('ZOOM', 7)
    .constant('DETAIL_ZOOM', 10)
    .constant('DEFAULT_MOVEME', 'Drag me!')
    .service('maps', [
        '$q',
        'leafletData',
        'satnetRPC',
        'ZOOM',
        'DETAIL_ZOOM',
        'T_OPACITY',
        'DEFAULT_MOVEME',
        function (
            $q,
            leafletData,
            satnetRPC,
            ZOOM,
            DETAIL_ZOOM,
            T_OPACITY,
            DEFAULT_MOVEME
        ) {

            'use strict';

            /**
             * Returns the mapInfo structure for the rest of the chained
             * promises.
             * @returns {$q} Promise that returns the mapInfo structure with
             *               a reference to the Leaflet map object.
             */
            this.getMainMap = function () {
                return leafletData.getMap('mainMap').then(function (m) {
                    return { map: m };
                });
            };

            this.getAddGSMap = function () {
                return leafletData.getMap('addGSMap').then(function (m) {
                    return { map: m };
                });
            };

            this.getEditGSMap = function () {
                return leafletData.getMap('editGSMap').then(function (m) {
                    return { map: m };
                });
            };

            /**
             * Redraws the Terminator to its new position.
             * @returns {*} Promise that returns the updated Terminator object.
             * @private
             */
            this.updateTerminator = function (t) {
                var t2 = L.terminator();
                t.setLatLngs(t2.getLatLngs());
                t.redraw();
                return t;
            };

            /**
             * Creates the main map and adds a terminator for the illuminated
             * surface of the Earth.
             * @returns {$q} Promise that returns the mapInfo object
             *               {map, terminator}.
             */
            this.createTerminatorMap = function () {
                var update_function = this.updateTerminator;
                return this.getMainMap().then(function (mapInfo) {
                    var t = L.terminator({ fillOpacity: T_OPACITY });
                    t.addTo(mapInfo.map);
                    mapInfo.terminator = t;
                    setInterval(function () { update_function(t); }, 500);
                    return mapInfo;
                });
            };

            /**
             * This promise returns a simple object with a reference to the
             * just created map.
             *
             * @param terminator If 'true' adds the overlaying terminator line.
             * @returns {$q} Promise that returns the 'mapData' structure with
             *               a reference to the Leaflet map and to the
             *               terminator overlaying line (if requested).
             */
            this.createMainMap = function (terminator) {

                var p = [];

                if (terminator) {
                    p.push(this.createTerminatorMap());
                } else {
                    p.push(this.getMainMap());
                }
                p.push(satnetRPC.getUserLocation());

                return $q.all(p).then(function (results) {
                    var ll = new L.LatLng(
                            results[1].latitude,
                            results[1].longitude
                        ),
                        map = results[0].map;

                    map.setView(ll, ZOOM);

                    return ({
                        map: results[0].map,
                        terminator: results[0].terminator,
                        center: {
                            lat: results[1].latitude,
                            lng: results[1].longitude
                        }
                    });

                });

            };

            /**
             * Initializes the map, centers it with the estimated position
             * of the user (GeoIP) and adds a "move-me" draggable marker.
             *
             * @param {L} map Reference to the Leaflet map.
             * @param {String} message Message to be added to the marker.
             * @returns {$q} Promise that returns the 'mapData' structure with
             *               an additional marker.
             */
            this.createMoveMeMap = function (map, message) {

                if (message === null) { message = DEFAULT_MOVEME; }

                return satnetRPC.getUserLocation().then(function (location) {
                    var lat = location.lat,
                        lng = location.lng,
                        ll = new L.LatLng(lat, lng),
                        marker = L.marker({
                            lat: lat,
                            lng: lng,
                            message: message,
                            focus: true,
                            draggable: true
                        });

                    map.setView(ll, DETAIL_ZOOM);
                    marker.addTo(map);

                    return ({
                        map: map,
                        marker: marker,
                        center: {
                            lat: location.lat,
                            lng: location.lng
                        }
                    });

                });

            };

            /**
             * Returns the base layers in the format required by the Angular
             * Leaflet plugin.
             *
             * @returns {{esri_baselayer: {name: string, type: string, url: string, layerOptions: {attribution: string}}, osm_baselayer: {name: string, type: string, url: string, layerOptions: {attribution: string}}}}
             */
            this.getBaseLayers = function () {
                return {
                    esri_baselayer: {
                        name: 'ESRI Base Layer',
                        type: 'xyz',
                        url: 'http://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',
                        layerOptions: {
                            noWrap: true,
                            attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ'
                        }
                    },
                    osm_baselayer: {
                        name: 'OSM Base Layer',
                        type: 'xyz',
                        url: 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                        layerOptions: {
                            noWrap: true,
                            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                        }
                    }
                };
            };

            /**
             * Returns the overlays in the format required by the Angular
             * Leaflet plugin.
             *
             * @returns {{oms_admin_overlay: {name: string, type: string, url: string, visible: boolean, layerOptions: {minZoom: number, maxZoom: number, attribution: string}}, hydda_roads_labels_overlay: {name: string, type: string, url: string, layerOptions: {minZoom: number, maxZoom: number, attribution: string}}, stamen_toner_labels_overlay: {name: string, type: string, url: string, layerOptions: {attribution: string, subdomains: string, minZoom: number, maxZoom: number}}, owm_rain_overlay: {name: string, type: string, url: string, layerOptions: {attribution: string, opacity: number}}, owm_temperature_overlay: {name: string, type: string, url: string, layerOptions: {attribution: string, opacity: number}}}}
             */
            this.getOverlays = function () {
                return {
                    oms_admin_overlay: {
                        name: 'Administrative Boundaries',
                        type: 'xyz',
                        url: 'http://openmapsurfer.uni-hd.de/tiles/adminb/x={x}&y={y}&z={z}',
                        visible: true,
                        layerOptions: {
                            noWrap: true,
                            minZoom: 0,
                            maxZoom: 19,
                            attribution: 'Imagery from <a href="http://giscience.uni-hd.de/">GIScience Research Group @ University of Heidelberg</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                        }
                    },
                    hydda_roads_labels_overlay: {
                        name: 'Roads and Labels',
                        type: 'xyz',
                        url: 'http://{s}.tile.openstreetmap.se/hydda/roads_and_labels/{z}/{x}/{y}.png',
                        layerOptions: {
                            noWrap: true,
                            minZoom: 0,
                            maxZoom: 18,
                            attribution: 'Tiles courtesy of <a href="http://openstreetmap.se/" target="_blank">OpenStreetMap Sweden</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                        }
                    },
                    stamen_toner_labels_overlay: {
                        name: 'Labels',
                        type: 'xyz',
                        url: 'http://{s}.tile.stamen.com/toner-labels/{z}/{x}/{y}.png',
                        layerOptions: {
                            noWrap: true,
                            attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
                            subdomains: 'abcd',
                            minZoom: 0,
                            maxZoom: 20
                        }
                    },
                    owm_rain_overlay: {
                        name: 'Rain',
                        type: 'xyz',
                        url: 'http://{s}.tile.openweathermap.org/map/rain/{z}/{x}/{y}.png',
                        layerOptions: {
                            noWrap: true,
                            attribution: 'Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>',
                            opacity: 0.35
                        }
                    },
                    owm_temperature_overlay: {
                        name: 'Temperature',
                        type: 'xyz',
                        url: 'http://{s}.tile.openweathermap.org/map/temp/{z}/{x}/{y}.png',
                        layerOptions: {
                            noWrap: true,
                            attribution: 'Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>',
                            opacity: 0.5
                        }
                    }
                };
            };

            /**
             * Returns a string with the data from a MapInfo like structure.
             *
             * @param   {Object} mapInfo The structure to be printed out.
             * @returns {String} Human-readable representation (string).
             */
            this.asString = function (mapInfo) {
                return 'mapInfo = {' +
                    '"center": ' + JSON.stringify(mapInfo.center) + ', ' +
                    '"terminator": ' + mapInfo.terminator + ', ' +
                    '"map": ' + mapInfo.map +
                    '}';
            };

        }
    ]);