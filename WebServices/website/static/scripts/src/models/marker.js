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

            this.getNgOverlays = function () {
                return {
                    'servers': {
                        name: 'Servers',
                        type: 'group',
                        visible: true,
                        layerOptions: {
                            layers: this.serverLayers.getLayers().concat(this.connectorLayers.getLayers())
                        }
                    },
                    'gss' : {
                        name: 'Ground Stations',
                        type: 'group',
                        visible: true,
                        layerOptions: {
                            layers: this.gsLayers.getLayers()
                        }
                    },
                    'sc' : {
                        name: 'Spacecraft',
                        type: 'group',
                        visible: true,
                        layerOptions: {
                            layers: this.scLayers.getLayers().concat(this.trackLayers.getLayers())
                        }
                    }
                };
            };

            /******************************************************************/
            /************************************************* SERVER MARKERS */
            /******************************************************************/

            this.serverLayers = L.layerGroup();
            this.servers = {};

            this.serverMarker = {
                draggable: false,
                icon: L.icon({
                    iconUrl: '/static/images/icons/server-icon.svg',
                    iconSize: [15, 15]
                })
            };

            /**
             * Creates a new marker for the given Network Server.
             * @param {String} identifier Identifier of the server.
             * @param {Number} latitude Server's estimated latitude.
             * @param {Number} longitude Server's estimated longitude.
             * @return {Object} Marker for this server.
             */
            this.createServerMarker = function (
                identifier,
                latitude,
                longitude
            ) {
                return L.marker(
                    L.latLng(latitude, longitude),
                    this.serverMarker
                ).bindLabel(identifier, { noHide: false });
            };

            /**
             * Adds a new server with the given ID and position (latitude,
             * longitude) to the map.
             * @param id Identifer of the server (usually the hostname).
             * @param latitude Latitude position.
             * @param longitude Longitude position.
             * @returns {*} Promise that returns the configuration..
             */
            this.addServer = function (id, latitude, longitude) {

                if (this.servers.hasOwnProperty(id)) {
                    throw '[x-maps] SERVER Marker already exists, id = ' + id;
                }
                console.log(
                    '>>> server = ' + id
                        + '@(' + latitude + ', ' + longitude + ')'
                );

                var m = this.createServerMarker(id, latitude, longitude);

                this.servers[id] = {
                    marker: m,
                    latitude: latitude,
                    longitude: longitude,
                    groundstations: []
                };
                this.serverLayers.addLayer(m);

                return maps.getMainMap().then(function (mapInfo) {
                    console.log('mapInfo.map + ' + mapInfo.map);
                    m.addTo(mapInfo.map);
                    return {
                        id: id,
                        latitude: latitude,
                        longitude: longitude,
                        marker: m
                    };
                });

            };

            /******************************************************************/
            /***************************************** GROUND STATION MARKERS */
            /******************************************************************/

            this.gs = {};
            this.gsLayers = L.layerGroup();
            this.connectors = {};
            this.connectorLayers = L.layerGroup();

            this.gsStyle = {
                draggable: false,
                icon: L.icon({
                    iconUrl: '/static/images/icons/gs-icon.svg',
                    iconSize: [15, 15]
                })
            };

            this.connectorStyle = {
                color: '#036128',
                weight: 2,
                opacity: 0.5
            };

            /**
             * Creates a new markerfor the given GroundStation object.
             * @param   {Object} cfg Configuration object for the new
             *                          GroundStation.
             * @returns {L.Marker}
             */
            this.createGSMarker = function (cfg) {
                return L.marker(
                    L.latLng(cfg.cfg.latitude, cfg.cfg.longitude),
                    this.gsStyle
                ).bindLabel(cfg.cfg.id, { noHide: true });
            };

            /**
             * This function creates a connection line object to be draw on the
             * map.
             *
             * @param {Object} gs Configuration object of the GroundStation.
             * @returns {*} L.polyline object
             *
             * TODO The structure for modelling what server owns each
             * TODO GroundStation has already started to be implemented. In the
             * TODO 'this.servers' dictionary, each entry has a field called
             * TODO 'groundstations' that enables the correct modelling of the
             * TODO network. Right now, the first server is always chosen and
             * TODO all the GroundStations are bound to it. In the future, each
             * TODO time a GroundStation is added, the server that it belongs
             * TODO to should be specified and used accordingly.
             */
            this.createGSConnector = function (gs) {

                var server, s_ids = Object.keys(this.servers);
                server = this.servers[s_ids[0]];

                return L.polyline(
                    this.calculateLineLatLngs(server, gs),
                    this.connectorStyle
                );

            };

            /**
             * Adds a marker to the main map.
             * @param id Identifier of the GroundStation.
             * @param gs Configuration object for the groundstastion.
             * @returns {*} Promise that returns the updated configuration.
             */
            this.addGS = function (id, gs) {

                if (this.gs.hasOwnProperty(id)) {
                    throw '[x-maps] GS Marker already exists, id = ' + id;
                }

                var m = this.createGSMarker(gs),
                    c = this.createGSConnector(gs);

                this.gs[id] = m;
                this.connectors[id] = c;
                this.gsLayers.addLayer(m);
                this.connectorLayers.addLayer(c);

                return maps.getMainMap().then(function (mapInfo) {
                    console.log('mapInfo.map + ' + mapInfo.map);
                    c.addTo(mapInfo.map);
                    m.addTo(mapInfo.map);
                    gs.marker = m;
                    gs.connector = c;
                    return gs;
                });

            };

            /**
             * Updates the configuration for the marker of the given GS.
             *
             * @param id The identififer of the GroundStation.
             * @param lat The new latitude for the marker.
             * @param lng The new longitude for the marker.
             * @returns {String} GroundStation identifier.
             */
            this.updateGS = function (id, lat, lng) {

                if (!this.gs.hasOwnProperty(id)) {
                    throw '[x-maps] Marker does NOT exist, id = ' + id;
                }

                var server,
                    s_ids = Object.keys(this.servers),
                    gs = this.gs[id];
                server = this.servers[s_ids[0]];

                gs.setLatLng(L.latLng(lat, lng));
                this.connectors[id].setLatLngs(
                    this.calculateLineLatLngs(server, gs)
                );

                return id;

            };

            /**
             * This function calculates the starting and ending point of the
             * Polylines to be used as connectors in between the GroundStations
             * and the servers of the network.
             *
             * @param server Server configuration object.
             * @param gs GroundStation configuration object.
             * @returns {[L.latlng]}
             */
            this.calculateLineLatLngs = function (server, gs) {
                var s_ll = [server.latitude, server.longitude],
                    g_ll = [gs.cfg.latitude, gs.cfg.longitude];
                return [ L.latLng(s_ll), L.latLng(g_ll)];
            };

            /**
             * Removes the marker from the main map and the connector associated
             * with this GroundStation (in case it exists, flexible approach).
             *
             * @param id Identifier of the GroundStation whose marker is to be
             *              removed.
             * @returns Promise that returns the id of the just removed
             *          GroundStation.
             */
            this.removeGS = function (id) {
                var marker = null, c = null;
                if (!this.gs.hasOwnProperty(id)) {
                    throw '[x-maps] Marker does NOT exist, id = ' + id;
                }

                if (this.connectors.hasOwnProperty(id)) {
                    c = this.connectors[id];
                    this.connectorLayers.removeLayer(c);
                    delete this.connectors[id];
                }

                marker = this.gs[id];
                this.gsLayers.removeLayer(marker);
                delete this.gs[id];

                return maps.getMainMap().then(function (mapInfo) {
                    mapInfo.map.removeLayer(marker);
                    if (c !== null) { mapInfo.map.removeLayer(c); }
                    return id;
                });
            };

            /******************************************************************/
            /********************************************* SPACECRAFT MARKERS */
            /******************************************************************/

            this.sc = {};
            this.scLayers = L.layerGroup();
            this.trackLayers = L.layerGroup();

            this.scStyle = {
                autostart: true,
                draggable: false,
                icon: L.icon({
                    iconUrl: '/static/images/icons/sc-icon.svg',
                    iconSize: [10, 10]
                })
            };

            this.trackStyle = {
                weight: 3,
                opacity: 0.25,
                steps: _GEOLINE_STEPS
            };

            this.colors = [ 'red', 'blue', 'yellow' ];
            this.color_n = 0;

            /**
             * For a given Spacecraft configuration object, it creates the
             * marker for the spacecraft, its associated label and the
             * groundtrack.
             *
             * @param id Identifier of the Spacecraft.
             * @param cfg Configuration object.
             * @returns {{marker: L.Marker.movingMarker, track: L.polyline}}
             */
            this.createSCMarkers = function (id, cfg) {

                var gt = this.readTrack(cfg.groundtrack),
                    mo = this.scStyle,
                    color =  this.colors[this.color_n % this.colors.length];
                this.color_n += 1;
                this.trackStyle.color = color;

                return {
                    marker: L.Marker.movingMarker(gt.positions, gt.durations, mo)
                        .bindLabel(id, { noHide: true }),
                    track: L.geodesic([gt.geopoints], this.trackStyle)
                };

            };

            /**
             * Finds the current point at which the marker has to be positioned.
             * Using the parameter {nowUs}, this function searchs for the
             * following point of the GroundTrack at which the Spacecraft is
             * supposed to be positioned.
             *
             * TODO Best unit testing for this algorithm.
             *
             * @param groundtrack RAW groundtrack from the server.
             * @param nowUs Now time in microsecnods.
             * @returns {number} Position of the array.
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
             * Function that reads the RAW groundtrack from the server and
             * transforms it into a usable one for the JS client.
             *
             * TODO What if the groundtrack has not started yet?
             * TODO A better unit testing for this algorithm.
             *
             * @param groundtrack RAW groundtrack from the server.
             * @returns {{durations: Array, positions: Array, geopoints: Array}}
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

            /**
             * Adds the markers for the new Spacecraft, this is: the marker for
             * the Spacecraft itself (together with its associated label) and
             * associated groundtrack geoline.
             *
             * @param id Identifier of the Spacecraft.
             * @param cfg Configuration for the Spacecraft.
             * @returns {{
             *              id: String,
             *              cfg: Object,
             *              marker: m.L.Marker.movingMarker,
             *              track: m.L.geodesic
             *          }}
             */
            this.addSC = function (id, cfg) {

                if (this.sc.hasOwnProperty(id)) {
                    throw '[x-maps] SC Marker already exists, id = ' + id;
                }

                var m = this.createSCMarkers(id, cfg);
                this.sc[id] = m;
                this.scLayers.addLayer(m.marker);
                this.trackLayers.addLayer(m.track);

                return maps.getMainMap().then(function (mapInfo) {
                    m.track.addTo(mapInfo.map);
                    m.marker.addTo(mapInfo.map);
                    return {
                        id: id,
                        cfg: cfg,
                        marker: m.marker,
                        track: m.track
                    };
                });

            };

            /**
             * Removes all the markers associated with this Spacecraft object.
             *
             * @param id Identifier of the Spacecraft.
             * @returns {String} Spacecraft identifier.
             */
            this.removeSC = function (id) {

                if (!this.sc.hasOwnProperty(id)) {
                    throw '[x-maps] Marker does NOT exist, id = ' + id;
                }

                var m = this.sc[id];
                this.scLayers.removeLayer(m.marker);
                this.trackLayers.removeLayer(m.track);
                delete this.sc[id];

                return maps.getMainMap().then(function (mapInfo) {
                    mapInfo.map.removeLayer(m.marker);
                    mapInfo.map.removeLayer(m.track);
                    return id;
                });

            };

        }
    ]);