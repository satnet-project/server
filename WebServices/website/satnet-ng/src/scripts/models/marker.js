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
angular.module('marker-models', ['map-services']);

/**
 * eXtended GroundStation models. Services built on top of the satnetRPC
 * service and the basic GroundStation models.
 */
angular.module('marker-models')
    .constant('_RATE', 1)
    .constant('_SIM_DAYS', 1)
    .constant('_GEOLINE_STEPS', 5)
    .service('markers', [
        '$log', 'maps', '_RATE', '_SIM_DAYS', '_GEOLINE_STEPS',
        function ($log, maps, _RATE, _SIM_DAYS, _GEOLINE_STEPS) {

            'use strict';

            /******************************************************************/
            /****************************************************** MAP SCOPE */
            /******************************************************************/

            // Structure that holds a reference to the map and to the
            // associated structures.
            this._mapInfo = null;
            // Scope where the leaflet angular pluing has its variables.
            this._mapScope = null;

            /**
             * Returns the current scope to which this markers service is bound
             * to.
             * @returns {null|*} The _mapScope object.
             */
            this.getScope = function () {
                if (this._mapScope === null) {
                    throw '<_mapScope> has not been set.';
                }
                return this._mapScope;
            };

            /**
             * Configures the scope of the Map controller to set the variables
             * for the angular-leaflet plugin.
             *
             * @param scope Scope ($scope) of the controller for the
             *              angular-leaflet plugin.
             */
            this.configureMapScope = function (scope) {

                this._mapScope = scope;

                angular.extend(this._mapScope, {
                    center: { lat: maps.LAT, lng: maps.LNG, zoom: maps.ZOOM },
                    layers: {
                        baselayers: {},
                        overlays: {}
                    },
                    markers: {},
                    paths: {},
                    maxbounds: {}
                });

                this._mapScope.layers.baselayers = angular.extend(
                    {},
                    this._mapScope.layers.baselayers,
                    maps.getBaseLayers()
                );

                this._mapScope.layers.overlays = angular.extend(
                    {},
                    maps.getOverlays(),
                    this.getOverlays()
                );

                var mapInfo = this._mapInfo;
                maps.createMainMap(true).then(function (data) {
                    $log.log(
                        '[map-controller] Created map = <' +
                            maps.asString(data) + '>'
                    );
                    mapInfo = angular.extend({}, mapInfo, data);
                });

            };

            /******************************************************************/
            /**************************************************** MARKER KEYS */
            /******************************************************************/

            this._KEY_HEADER = 'MK'; // "MK" stands for "marker key"
            this._key_number = 0;

            /**
             * Dictionary that contains the relation between the identifiers
             * of the objects and the keys for the markers that represent those
             * objects.
             * @type {{}}
             */
            this._ids2keys = {};

            /**
             * Creates a new key for the given identifier and adds it to the
             * dictionary of identifiers and keys.
             * @param identifier Identifier of the marker.
             * @returns {string} Key for accessing to the marker.
             */
            this.createMarkerKey = function (identifier) {

                if (this._ids2keys[identifier] !== undefined) {
                    return this.getMarkerKey(identifier);
                }

                var key = this._KEY_HEADER + this._key_number;
                this._key_number += 1;
                this._ids2keys[identifier] = key;
                return key;

            };

            /**
             * Returns the key for the given object that holds a marker.
             * @param identifier Identifier of the object.
             * @returns {string} Key for accessing to the marker.
             */
            this.getMarkerKey = function (identifier) {
                return this._ids2keys[identifier];
            };

            /**
             * Returns the marker for the server, in case it exists!
             *
             * @param gs_identifier Identifier of the GroundStation object that
             *                      is bound to the server.
             * @returns {null|*} String with the key for the marker of the
             *                      server.
             */
            this.getServerMarker = function (gs_identifier) {
                if (this._serverMarkerKey === null) {
                    throw 'No server has been defined';
                }
                console.log('@markers.getServerMarker, id = ' + gs_identifier);
                return this.getScope().markers[this._serverMarkerKey];
            };

            /**
             * Returns the marker for the object with the given identifier.
             *
             * @param identifier Identifier of the object, which can be either
             *                      a GroundStation, a Spacecraft or a Server.
             * @returns {*} Marker object.
             */
            this.getMarker = function (identifier) {
                return this.getScope().markers[this.getMarkerKey(identifier)];
            };

            /**
             * Returns the overlays to be included as markerclusters within
             * the map.
             *
             * @returns {{servers: {name: string, type: string, visible: boolean}, groundstations: {name: string, type: string, visible: boolean}, spacecraft: {name: string, type: string, visible: boolean}}}
             */
            this.getOverlays = function () {
                return {
                    network : {
                        name: 'Network',
                        type: 'markercluster',
                        visible: true
                    },
                    groundstations: {
                        name: 'Ground Stations',
                        type: 'markercluster',
                        visible: true
                    }
                    /*, TODO Native angular-leaflet support for MovingMarker
                    spacecraft: {
                        name: 'Spacecraft',
                        type: 'markercluster',
                        visible: true
                    }
                    */
                };
            };

            /******************************************************************/
            /***************************************** NETWORK SERVER MARKERS */
            /******************************************************************/

            this._serverMarkerKey = null;

            /**
             * Creates a new marker for the given Network Server.
             * @param {String} id Identifier of the server.
             * @param {Number} latitude Server's estimated latitude.
             * @param {Number} longitude Server's estimated longitude.
             *
             * TODO Check possible bug: when 'noHide = false', once the layer
             * TODO is removed, the label does not appear again when the mouse
             * TODO is over the icon.
             */
            this.createServerMarker = function (id, latitude, longitude) {
                this._serverMarkerKey = this.createMarkerKey(id);
                this.getScope().markers[this._serverMarkerKey] = {
                    lat: latitude,
                    lng: longitude,
                    focus: true,
                    draggable: false,
                    layer: 'network',
                    icon: {
                        iconUrl: '/static/images/server-icon.svg',
                        iconSize: [15, 15]
                    },
                    label: {
                        message: id,
                        options: {
                            noHide: true
                        }
                    },
                    groundstations: [],
                    identifier: id
                };
                return id;
            };

            /******************************************************************/
            /***************************************** GROUND STATION MARKERS */
            /******************************************************************/

            /**
             * Creates a unique identifier for the connector of this
             * GroundStation and the Standalone network server.
             *
             * @param gs_identifier Identifier of the GroundStation object.
             * @returns {string} Identifier for the connector.
             */
            this.createConnectorIdentifier = function (gs_identifier) {
                return 'connect:' + gs_identifier + '_2_' +
                    this.getServerMarker(gs_identifier).identifier;
            };

            /**
             * This function creates a connection line object to be draw on the
             * map in between the provided Server and the Ground Station
             * objects.
             *
             * @param {Object} gs_identifier Identifier of the GroundStation
             *                                  object.
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
            this.createGSConnector = function (gs_identifier) {

                var s_marker = this.getServerMarker(gs_identifier),
                    g_marker = this.getMarker(gs_identifier),
                    c_id = this.createConnectorIdentifier(gs_identifier),
                    c_key,
                    r = {};

                c_key = this.createMarkerKey(c_id);
                r[c_key] = {
                    layer: 'network',
                    color: '#036128',
                    type: 'polyline',
                    weight: 2,
                    opacity: 0.5,
                    latlngs: [s_marker, g_marker],
                    identifier: c_id
                };

                this.getScope().paths =
                    angular.extend({}, this.getScope().paths, r);
                return c_id;

            };

            /**
             * Creates a new marker object for the given GroundStation.
             *
             * @param cfg The configuration of the GroundStation.
             * @returns Angular leaflet marker.
             */
            this.createGSMarker = function (cfg) {

                var id = cfg.groundstation_id;

                this.getScope().markers[this.createMarkerKey(id)] = {
                    lat: cfg.groundstation_latlon[0],
                    lng: cfg.groundstation_latlon[1],
                    focus: true,
                    draggable: false,
                    layer: 'groundstations',
                    icon: {
                        iconUrl: '/static/images/gs-icon.svg',
                        iconSize: [15, 15]
                    },
                    label: {
                        message: cfg.groundstation_id,
                        options: {
                            noHide: true
                        }
                    },
                    identifier: id
                };

                this.createGSConnector(id);
                return id;

            };

            /**
             * Updates the configuration for the markers of the given
             * GroundStation object.
             *
             * @param cfg New configuration of the object.
             * @returns {cfg.groundstation_id|*} Identifier.
             *
             * TODO Validate
             */
            this.updateGSMarker = function (cfg) {
                var new_lat = cfg.groundstation_latlon[0],
                    new_lng = cfg.groundstation_latlon[1],
                    marker = this.getMarker(cfg.groundstation_id);
                if (marker.lat !== new_lat) {
                    marker.lat = new_lat;
                }
                if (marker.lng !== new_lng) {
                    marker.lng = new_lng;
                }
                return cfg.groundstation_id;
            };

            /**
             * Removes a given GroundStation marker, together with its
             * associated connector path to the server and with the identifier
             * within the servers lists of bounded GroundStations.
             *
             * @param identifier Identifier of the GroundStation whose markers
             *                      are going to be removed.
             */
            this.removeGSMarker = function (identifier) {
                console.log('@removeGSMarker!!!');
                var p_key = this.getMarkerKey(
                        this.createConnectorIdentifier(identifier)
                    ),
                    m_key = this.getMarkerKey(identifier);
                console.log('@removeGSMarker, c_id = ' +  this.createConnectorIdentifier(identifier));
                console.log('@removeGSMarker, p_key = ' + p_key);
                console.log('@removeGSMarker, m_key = ' + m_key);
                delete this.getScope().paths[p_key];
                delete this.getScope().markers[m_key];
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
                    iconUrl: '/static/images/sc-icon.svg',
                    iconSize: [10, 10]
                })
            };

            this.trackStyle = {
                weight: 3,
                opacity: 0.25,
                steps: _GEOLINE_STEPS
            };

            this.colors = ['red', 'blue', 'yellow'];
            this.color_n = 0;

            /**
             * For a given Spacecraft configuration object, it creates the
             * marker for the spacecraft, its associated label and the
             * groundtrack.
             *
             * @param cfg Configuration object.
             * @returns {{marker: L.Marker.movingMarker, track: L.polyline}}
             */
            this.createSCMarkers = function (cfg) {

                var id = cfg.spacecraft_id,
                    gt = this.readTrack(cfg.groundtrack),
                    mo = this.scStyle,
                    color =  this.colors[this.color_n % this.colors.length];
                this.color_n += 1;
                this.trackStyle.color = color;

                return {
                    marker: L.Marker.movingMarker(
                        gt.positions,
                        gt.durations,
                        mo
                    ).bindLabel(id, { noHide: true }),
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
             * Updates the configuration for a given Spacecraft object.
             *
             * @param cfg Object with the new configuration for the Spacecraft.
             * @returns {String} Identifier of the just-updated Spacecraft.
             *
             * TODO Real spacecraft update.
             */
            this.updateSC = function (cfg) {

                var id = cfg.spacecraft_id;
                if (!this.sc.hasOwnProperty(id)) {
                    throw '[x-maps] SC Marker does not exist! id = ' + id;
                }

                console.log('@markers.updateSC, cfg = ' + JSON.stringify(cfg));
                return id;

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