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
angular.module('marker-models', [
    'map-services'
]);

/**
 * eXtended GroundStation models. Services built on top of the satnetRPC
 * service and the basic GroundStation models.
 */
angular.module('marker-models')
    .constant('_RATE', 1)
    .constant('_SIM_DAYS', 1)
    .constant('_GEOLINE_STEPS', 5)
    .service('markers', [
        'maps', '_RATE', '_SIM_DAYS', '_GEOLINE_STEPS',
        function (maps, _RATE, _SIM_DAYS, _GEOLINE_STEPS) {

            'use strict';

            this.gs = {};
            this.gsMarker = {
                draggable: false,
                icon: L.icon({
                    iconUrl: '/static/images/icons/gs-icon.svg',
                    iconSize: [15, 15]
                })
            };

            /**
             * Creates a new entrance in the configuration structure.
             * @param   {String} id Identifier of the new GroundStation.
             * @param   {Object} cfg Configuration object for the new
             *                          GroundStation.
             * @returns {Object} Returns an object with the marker and the
             *                  configuration.
             */
            this.createGS = function (id, cfg) {
                return L.marker(
                    L.latLng(cfg.cfg.latitude, cfg.cfg.longitude),
                    this.gsMarker
                ).bindLabel(id, { noHide: true });
            };

            /**
             * Adds a marker to the main map.
             * @param id Identifier of the GroundStation.
             * @param gs Configuration object for the groundstastion.
             * @returns {*} Promise that returns the updated configuration object.
             */
            this.addGS = function (id, gs) {
                if (this.gs.hasOwnProperty(id)) {
                    throw '[x-maps] GS Marker already exists, id = ' + id;
                }
                console.log('>>> gs = ' + JSON.stringify(gs));
                var m = this.createGS(id, gs);
                this.gs[id] = m;
                return maps.getMainMap().then(function (mapInfo) {
                    console.log('mapInfo.map + ' + mapInfo.map);
                    m.addTo(mapInfo.map);
                    return { id: id, cfg: gs, marker: m };
                });
            };

            /**
             * Updates the configuration for the marker of the given GS.
             * @param id The identififer of the GroundStation.
             * @param lat The new latitude for the marker.
             * @param lng The new longitude for the marker.
             */
            this.updateGS = function (id, lat, lng) {
                if (!this.gs.hasOwnProperty(id)) {
                    throw '[x-maps] Marker does NOT exist, id = ' + id;
                }
                this.gs[id].setLatLng(L.latLng(lat, lng));
            };

            /**
             * Removes the marker from the main map.
             * @param id Identifier of the GroundStation whose marker is to be
             *              removed.
             * @returns Promise that returns the id of the just removed
             *          GroundStation.
             */
            this.removeGS = function (id) {
                if (!this.gs.hasOwnProperty(id)) {
                    throw '[x-maps] Marker does NOT exist, id = ' + id;
                }
                var marker = this.gs[id];
                delete this.gs[id];
                return maps.getMainMap().then(function (mapInfo) {
                    mapInfo.map.removeLayer(marker);
                    return id;
                });
            };

            this.sc = {};
            this.scMarker = {
                autostart: true,
                draggable: false,
                icon: L.icon({
                    iconUrl: '/static/images/icons/sc-icon.svg',
                    iconSize: [10, 10]
                })
            };

            this.colors = [
                'red', 'blue', 'black'
            ];
            this.color_n = 0;

            this.createSC = function (id, cfg) {

                var gt = this.readTrack(cfg.groundtrack),
                    mo = this.scMarker,
                    color =  this.colors[this.color_n % this.colors.length];
                this.color_n += 1;

                return {
                    marker: L.Marker.movingMarker(gt.positions, gt.durations, mo)
                        .bindLabel(id, { noHide: true }),
                    track: L.geodesic(
                        [gt.geopoints],
                        {
                            weight: 3,
                            opacity: 0.25,
                            color: color,
                            steps: _GEOLINE_STEPS
                        }
                    )
                };

            };

            /**
             * TODO Best unit testing for this algorithm.
             * @param groundtrack
             * @param nowUs
             * @returns {number}
             */
            this.findPrevious = function (groundtrack, nowUs) {
                var i;
                for (i = 0; i < groundtrack.length; i += 1) {
                    if (groundtrack[i].timestamp > nowUs) {
                        return i - 1;
                    }
                }
                throw 'GroundTrack is too old!';
            };

            /**
             * TODO What if the groundtrack has not started yet?
             * TODO A better unit testing for this algorithm.
             * @param groundtrack
             * @returns {{durations: Array, positions: Array}}
             */
            this.readTrack = function (groundtrack) {
                var nowUs = Date.now() * 1000,
                    endUs = moment().add(_SIM_DAYS, "days")
                        .toDate().getTime() * 1000,
                    startIndex = this.findPrevious(groundtrack, nowUs),
                    endIndex = this.findPrevious(groundtrack, endUs),
                    j,
                    durations = [],
                    positions = [],
                    geopoints = [];

                console.log('>>> nowMS = ' + nowUs);
                console.log('>>> endMS = ' + endUs);
                console.log('>>> startIndex = ' + startIndex);
                console.log('>>> endIndex = ' + endIndex);

                if (startIndex !== 0) {
                    startIndex = startIndex - 1;
                }
                positions.push([
                    groundtrack[startIndex].latitude,
                    groundtrack[startIndex].longitude
                ]);
                for (j = startIndex; j < endIndex; j += 1) {
                    durations.push((
                        groundtrack[j + 1].timestamp - groundtrack[j].timestamp
                    ) / 1000);
                    positions.push([
                        groundtrack[j + 1].latitude,
                        groundtrack[j + 1].longitude
                    ]);
                    if (j % _RATE === 0) {
                        geopoints.push(
                            new L.LatLng(
                                groundtrack[j + 1].latitude,
                                groundtrack[j + 1].longitude
                            )
                        );
                    }
                }

                return {
                    durations: durations,
                    positions: positions,
                    geopoints: geopoints
                };

            };

            this.addSC = function (id, cfg) {
                if (this.sc.hasOwnProperty(id)) {
                    throw '[x-maps] SC Marker already exists, id = ' + id;
                }
                var m = this.createSC(id, cfg);
                this.sc[id] = m;
                return maps.getMainMap().then(function (mapInfo) {
                    m.track.addTo(mapInfo.map);
                    m.marker.addTo(mapInfo.map);
                    return { id: id, cfg: cfg, marker: m };
                });
            };

            this.removeSC = function (id) {
                if (!this.sc.hasOwnProperty(id)) {
                    throw '[x-maps] Marker does NOT exist, id = ' + id;
                }
                var m = this.sc[id];
                delete this.sc[id];
                return maps.getMainMap().then(function (mapInfo) {
                    mapInfo.map.removeLayer(m.marker);
                    mapInfo.map.removeLayer(m.track);
                    return id;
                });
            };

        }
    ]);