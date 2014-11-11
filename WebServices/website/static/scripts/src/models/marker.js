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
angular.module('marker-models').service('markers', [
    'maps', function (maps) {

        'use strict';

        this.gs = {};
        this.sc = {};

        /**
         * Creates a new entrance in the configuration structure.
         * @param   {String} id Identifier of the new GroundStation.
         * @param   {Object} cfg Configuration object for the new GroundStation.
         * @returns {Object} Returns an object with the marker and the configuration.
         */
        this.createGS = function (id, cfg) {
            return L.marker(
                L.latLng(cfg.cfg.latitude, cfg.cfg.longitude),
                {
                    draggable: false,
                    icon: L.icon({
                        iconUrl: '/static/images/icons/gs-icon.svg',
                        iconSize: [30, 30]
                    })
                }
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
         * @returns {$q} Promise that returns the id of the just removed
         *                  GroundStation.
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

    }
]);