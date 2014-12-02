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

/**
 * Redraws the Terminator to its new position.
 * @returns {*} Promise that returns the updated Terminator object.
 * @private
 */
function updateTerminator(t) {
    'use strict';
    var t2 = L.terminator();
    t.setLatLngs(t2.getLatLngs());
    t.redraw();
    return t;
}

/** Module definition (empty array is vital!). */
angular.module('map-services', [ 'leaflet-directive', 'common' ]);

angular.module('map-services')
    .constant('T_OPACITY', 0.125)
    .constant('ZOOM', 7)
    .constant('DETAIL_ZOOM', 10)
    .constant('DEFAULT_MOVEME', 'Drag me!')
    .service('maps', [

        '$q', 'common', 'leafletData',
        'ZOOM', 'DETAIL_ZOOM', 'T_OPACITY', 'DEFAULT_MOVEME',
        function (
            $q,
            common,
            leafletData,
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
             * Creates the main map and adds a terminator for the illuminated
             * surface of the Earth.
             * @returns {$q} Promise that returns the mapInfo object
             *               {map, terminator}.
             */
            this.createTerminatorMap = function () {
                return this.getMainMap().then(function (mapInfo) {
                    var t = L.terminator({ fillOpacity: T_OPACITY });
                    t.addTo(mapInfo.map);
                    mapInfo.terminator = t;
                    setInterval(function () { updateTerminator(t); }, 500);
                    return mapInfo;
                });
            };

            /**
             * This promise returns a simple object with a reference to the
             * just created map.
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
                p.push(common.getUserLocation());

                return $q.all(p).then(function (results) {
                    var ll = new L.LatLng(results[1].lat, results[1].lng);
                    results[0].map.setView(ll, ZOOM);
                    return ({
                        map: results[0].map,
                        terminator: results[0].terminator,
                        center: {
                            lat: results[1].lat,
                            lng: results[1].lng
                        }
                    });
                });

            };

            /**
             * Initializes the map, centers it with the estimated position
             * of the user (GeoIP) and adds a "move-me" draggable marker.
             * @param {L} map Reference to the Leaflet map.
             * @param {String} message Message to be added to the marker.
             * @returns {$q} Promise that returns the 'mapData' structure with
             *               an additional marker.
             */
            this.createMoveMeMap = function (map, message) {

                if (message === null) {
                    message = DEFAULT_MOVEME;
                }

                return common.getUserLocation().then(function (location) {
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
             * Returns a string with the data from a MapInfo like structure.
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