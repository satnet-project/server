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
angular.module('pushServices', []);

/**
 * Service that defines the basic calls to the services of the SATNET network
 * through JSON RPC. It defines a common error handler for all the errors that
 * can be overriden by users.
 */
angular.module('pushServices').service('satnetPush', [
    '$log', '$pusher',
    function ($log, $pusher) {
        'use strict';

        this._API_KEY = '79bee37791b6c60f3e56';

        this._client = null;
        this._service = null;

        // Names of the channels for subscription
        this.DOWNLINK_CHANNEL = 'downlink';
        this.EVENTS_CHANNEL = 'events';
        // List of events that an application can get bound to.
        this.FRAME_EVENT = '+frame';
        this.GS_ADDED_EVENT = '+gs';
        this.GS_REMOVED_EVENT = '-gs';
        this.GS_UPDATED_EVENT = '*gs';

        // List of channels that the service automatically subscribes to.
        this._channel_names = [
            'test_channel',
            this.DOWNLINK_CHANNEL,
            this.EVENTS_CHANNEL
        ];

        /**
         * Initializes the pusher service.
         * @private
         */
        this._init = function () {

            this._client = new Pusher(this._API_KEY, { encrypted: true });
            this._service = $pusher(this._client);
            this._service.connection.bind('state_change', this._logConnection);
            $log.info('[push] pusher.com service initialized!');

            this._subscribeChannels();

        };

        /**
         * Logs changes in the connection state for the pusher service.
         * @param states State changes
         * @private
         */
        this._logConnection = function (states) {
            $log.warn(
                '[push] State connection change, states = ' +
                    JSON.stringify(states)
            );
        };


        /**
         * Subscribe this service to all the channels whose names are part of
         * the "_channel_names_ array.
         * @private
         */
        this._subscribeChannels = function () {
            var self = this;
            angular.forEach(this._channel_names, function (name) {
                self._service.subscribe(name);
                $log.info('[push] Subscribed to channel <' + name + '>');
            });
        };

        /**
         * Method that binds the given function to the events triggered by
         * that channel.
         * @param channel_name Name of the channel
         * @param event_name Name of the event
         * @param callback_fn Function to be executed when that event happens
         */
        this.bind = function (channel_name, event_name, callback_fn) {
            if (!this._service.allChannels().hasOwnProperty(channel_name)) {
                throw 'Not subscribed to this channel, name = ' + channel_name;
            }
            this._service.channel(channel_name).bind(event_name, callback_fn);
        };

        /**
         * Binds the given callback function to the reception of any event
         * frames on the downlink channel.
         * @param callback_fn Callback function to be bound
         */
        this.bindFrameReceived = function (callback_fn) {
            this.bind(this.DOWNLINK_CHANNEL, this.FRAME_EVENT, callback_fn);
        };

        /**
         * Binds a callback function to the event with the name provided and
         * triggered through the specific events channel.
         * @param name Name of the event
         * @param callback_fn Callback function
         */
        this.bindEvent = function (name, callback_fn) {
            this.bind(this.EVENTS_CHANNEL, name, callback_fn);
        };

        this.bindGSAdded = function (callback_fn) {
            this.bindEvent(this.GS_ADDED_EVENT, callback_fn);
        };
        this.bindGSRemoved = function (callback_fn) {
            this.bindEvent(this.GS_REMOVED_EVENT, callback_fn);
        };
        this.bindGSUpdated = function (callback_fn) {
            this.bindEvent(this.GS_UPDATED_EVENT, callback_fn);
        };

        this._init();

    }

]);;/**
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
angular.module('celestrak-services', []);

/**
 * CELESTRAK service that permits retrieving the TLE's for the spacecraft from
 * the information at celestrak.com. It uses a CORSS proxy to avoid that
 * limitation.
 */
angular.module('celestrak-services').service('celestrak', [function () {

    'use strict';

    // Base URL
    this.CELESTRAK_URL_BASE = 'http://celestrak.com/NORAD/elements/';
    //this.CELESTRAK_URL_BASE = 'https://satnet.aero.calpoly.edu/celestrak/';
    // Weather and Earth Resources
    this.CELESTRAK_SECTION_1 = 'Weather & Earth Resources';
    this.CELESTRAK_WEATHER = this.CELESTRAK_URL_BASE + 'weather.txt';
    this.CELESTRAK_NOAA = this.CELESTRAK_URL_BASE + 'noaa.txt';
    this.CELESTRAK_GOES = this.CELESTRAK_URL_BASE + 'goes.txt';
    this.CELESTRAK_EARTH_RESOURCES = this.CELESTRAK_URL_BASE + 'resource.txt';
    this.CELESTRAK_SARSAT = this.CELESTRAK_URL_BASE + 'sarsat.txt';
    this.CELESTRAK_DISASTER_MONITORING = this.CELESTRAK_URL_BASE + 'dmc.txt';
    this.CELESTRAK_TRACKING_DATA_RELAY = this.CELESTRAK_URL_BASE + 'tdrss.txt';
    this.CELESTRAK_ARGOS = this.CELESTRAK_URL_BASE + 'argos.txt';
    // Communications
    this.CELESTRAK_SECTION_2 = 'Communications';
    this.CELESTRAK_GEOSTATIONARY = this.CELESTRAK_URL_BASE + 'geo.txt';
    this.CELESTRAK_INTELSAT = this.CELESTRAK_URL_BASE + 'intelsat.txt';
    this.CELESTRAK_GORIZONT = this.CELESTRAK_URL_BASE + 'gorizont.txt';
    this.CELESTRAK_RADUGA = this.CELESTRAK_URL_BASE + 'raduga.txt';
    this.CELESTRAK_MOLNIYA = this.CELESTRAK_URL_BASE + 'molniya.txt';
    this.CELESTRAK_IRIDIUM = this.CELESTRAK_URL_BASE + 'iridium.txt';
    this.CELESTRAK_ORBCOMM = this.CELESTRAK_URL_BASE + 'orbcomm.txt';
    this.CELESTRAK_GLOBALSTAR = this.CELESTRAK_URL_BASE + 'globalstar.txt';
    this.CELESTRAK_AMATEUR_RADIO = this.CELESTRAK_URL_BASE + 'amateur.txt';
    this.CELESTRAK_EXPERIMENTAL = this.CELESTRAK_URL_BASE + 'x-comm.txt';
    this.CELESTRAK_COMMS_OTHER = this.CELESTRAK_URL_BASE + 'other-comm.txt';
    // Navigation
    this.CELESTRAK_SECTION_3 = 'Navigation';
    this.CELESTRAK_GPS_OPERATIONAL = this.CELESTRAK_URL_BASE + 'gps-ops.txt';
    this.CELESTRAK_GLONASS_OPERATIONAL = this.CELESTRAK_URL_BASE + 'glo-ops.txt';
    this.CELESTRAK_GALILEO = this.CELESTRAK_URL_BASE + 'galileo.txt';
    this.CELESTRAK_BEIDOU = this.CELESTRAK_URL_BASE + 'beidou.txt';
    this.CELESTRAK_SATELLITE_AUGMENTATION = this.CELESTRAK_URL_BASE + 'sbas.txt';
    this.CELESTRAK_NNSS = this.CELESTRAK_URL_BASE + 'nnss.txt';
    this.CELESTRAK_RUSSIAN_LEO_NAVIGATION = this.CELESTRAK_URL_BASE + 'musson.txt';
    // Scientific
    this.CELESTRAK_SECTION_4 = 'Scientific';
    this.CELESTRAK_SPACE_EARTH_SCIENCE = this.CELESTRAK_URL_BASE + 'science.txt';
    this.CELESTRAK_GEODETIC = this.CELESTRAK_URL_BASE + 'geodetic.txt';
    this.CELESTRAK_ENGINEERING = this.CELESTRAK_URL_BASE + 'engineering.txt';
    this.CELESTRAK_EDUCATION = this.CELESTRAK_URL_BASE + 'education.txt';
    // Miscellaneous
    this.CELESTRAK_SECTION_5 = 'Miscellaneous';
    this.CELESTRAK_MILITARY = this.CELESTRAK_URL_BASE + 'military.txt';
    this.CELESTRAK_RADAR_CALLIBRATION = this.CELESTRAK_URL_BASE + 'radar.txt';
    this.CELESTRAK_CUBESATS = this.CELESTRAK_URL_BASE + 'cubesat.txt';
    this.CELESTRAK_OTHER = this.CELESTRAK_URL_BASE + 'other.txt';
    // CELESTRAK resources within a structured data type...
    this.CELESTRAK_RESOURCES = {
        'Weather': this.CELESTRAK_WEATHER,
        'NOAA': this.CELESTRAK_NOAA,
        'GOES': this.CELESTRAK_GOES,
        'Earth Resources': this.CELESTRAK_EARTH_RESOURCES,
        'SARSAT': this.CELESTRAK_SARSAT,
        'Disaster Monitoring': this.CELESTRAK_DISASTER_MONITORING,
        'Tracking & Data Relay': this.CELESTRAK_TRACKING_DATA_RELAY,
        'ARGOS': this.CELESTRAK_ARGOS,
        'Geostationary': this.CELESTRAK_GEOSTATIONARY,
        'Intelsat': this.CELESTRAK_INTELSAT,
        'Gorizont': this.CELESTRAK_GORIZONT,
        'Raduga': this.CELESTRAK_RADUGA,
        'Molniya': this.CELESTRAK_MOLNIYA,
        'Iridium': this.CELESTRAK_IRIDIUM,
        'Orbcomm': this.CELESTRAK_ORBCOMM,
        'Globalstar': this.CELESTRAK_GLOBALSTAR,
        'Amateur Radio': this.CELESTRAK_AMATEUR_RADIO,
        'Experimental': this.CELESTRAK_EXPERIMENTAL,
        'Others': this.CELESTRAK_COMMS_OTHER,
        'GPS Operational': this.CELESTRAK_GPS_OPERATIONAL,
        'Glonass Operational': this.CELESTRAK_GLONASS_OPERATIONAL,
        'Galileo': this.CELESTRAK_GALILEO,
        'Beidou': this.CELESTRAK_BEIDOU,
        'Satellite-based Augmentation System': this.CELESTRAK_SATELLITE_AUGMENTATION,
        'Navy Navigation Satellite System': this.CELESTRAK_NNSS,
        'Russian LEO Navigation': this.CELESTRAK_RUSSIAN_LEO_NAVIGATION,
        'Space & Earth Science': this.CELESTRAK_SPACE_EARTH_SCIENCE,
        'Geodetic': this.CELESTRAK_GEODETIC,
        'Engineering': this.CELESTRAK_ENGINEERING,
        'Education': this.CELESTRAK_EDUCATION,
        'Military': this.CELESTRAK_MILITARY,
        'Radar Callibration': this.CELESTRAK_RADAR_CALLIBRATION,
        'CubeSats': this.CELESTRAK_CUBESATS,
        'Other': this.CELESTRAK_OTHER
    };

    this.CELESTRAK_SELECT_SECTIONS = [
        /////////////////////////////////////////////////////////////////  SECTION 1
        { 'section': this.CELESTRAK_SECTION_1, 'subsection': 'Weather' },
        { 'section': this.CELESTRAK_SECTION_1, 'subsection': 'NOAA' },
        { 'section': this.CELESTRAK_SECTION_1, 'subsection': 'GOES' },
        { 'section': this.CELESTRAK_SECTION_1, 'subsection': 'Earth Resources' },
        { 'section': this.CELESTRAK_SECTION_1, 'subsection': 'SARSAT' },
        { 'section': this.CELESTRAK_SECTION_1, 'subsection': 'Disaster Monitoring' },
        { 'section': this.CELESTRAK_SECTION_1, 'subsection': 'Tracking & Data Relay' },
        { 'section': this.CELESTRAK_SECTION_1, 'subsection': 'ARGOS' },
        /////////////////////////////////////////////////////////////////  SECTION 2
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Geostationary' },
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Intelsat' },
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Gorizont' },
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Raduga' },
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Molniya' },
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Iridium' },
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Orbcomm' },
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Globalstar' },
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Amateur Radio' },
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Experimental' },
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Others' },
        /////////////////////////////////////////////////////////////////  SECTION 3
        { 'section': this.CELESTRAK_SECTION_3, 'subsection': 'GPS Operational' },
        { 'section': this.CELESTRAK_SECTION_3, 'subsection': 'Glonass Operational' },
        { 'section': this.CELESTRAK_SECTION_3, 'subsection': 'Galileo' },
        { 'section': this.CELESTRAK_SECTION_3, 'subsection': 'Beidou' },
        { 'section': this.CELESTRAK_SECTION_3, 'subsection': 'Satellite-based Augmentation System' },
        { 'section': this.CELESTRAK_SECTION_3, 'subsection': 'Navy Navigation Satellite System' },
        { 'section': this.CELESTRAK_SECTION_3, 'subsection': 'Russian LEO Navigation' },
        /////////////////////////////////////////////////////////////////  SECTION 4
        { 'section': this.CELESTRAK_SECTION_4, 'subsection': 'Space & Earth Science' },
        { 'section': this.CELESTRAK_SECTION_4, 'subsection': 'Geodetic' },
        { 'section': this.CELESTRAK_SECTION_4, 'subsection': 'Engineering' },
        { 'section': this.CELESTRAK_SECTION_4, 'subsection': 'Education' },
        /////////////////////////////////////////////////////////////////  SECTION 5
        { 'section': this.CELESTRAK_SECTION_5, 'subsection': 'Military' },
        { 'section': this.CELESTRAK_SECTION_5, 'subsection': 'Radar Callibration' },
        { 'section': this.CELESTRAK_SECTION_5, 'subsection': 'CubeSats' },
        { 'section': this.CELESTRAK_SECTION_5, 'subsection': 'Other' }
    ];

}]);;/**
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
angular.module('broadcaster', []);

/**
 * Service used for broadcasting UI events in between controllers.
 */
angular.module('broadcaster').service('broadcaster', [ '$rootScope',
    function ($rootScope) {

        'use strict';

        this.GS_ADDED_EVENT = 'gs.added';
        this.GS_REMOVED_EVENT = 'gs.removed';
        this.GS_UPDATED_EVENT = 'gs.updated';

        /**
         * Function that broadcasts the event associated with the creation of a
         * new GroundStation.
         * @param identifier The identifier of the GroundStation.
         */
        this.gsAdded = function (identifier) {
            $rootScope.$broadcast(this.GS_ADDED_EVENT, identifier);
        };

        /**
         * Function that broadcasts the event associated with the removal of a
         * new GroundStation.
         * @param identifier The identifier of the GroundStation.
         */
        this.gsRemoved = function (identifier) {
            console.log('@broadcaster.gsRemoved, id = ' + identifier);
            $rootScope.$broadcast(this.GS_REMOVED_EVENT, identifier);
        };

        /**
         * Function that broadcasts the event associated with the update of
         * new GroundStation.
         * @param identifier The identifier of the GroundStation.
         */
        this.gsUpdated = function (identifier) {
            $rootScope.$broadcast(this.GS_UPDATED_EVENT, identifier);
        };

        this.gsAddedPusher = function (id_object) {
            console.log(
                '[broadcaster] id_object = ' + JSON.stringify(id_object)
            );
            this.gsAdded(id_object.identifier);
        };
        this.gsRemovedPusher = function (id_object) {
            this.gsRemoved(id_object.identifier);
        };
        this.gsUpdatedPusher = function (id_object) {
            this.gsUpdated(id_object.identifier);
        };

        this.SC_ADDED_EVENT = 'sc.added';
        this.SC_REMOVED_EVENT = 'sc.removed';
        this.SC_UPDATED_EVENT = 'sc.updated';

        /**
         * Function that broadcasts the event associated with the creation of a
         * new Spacececraft.
         * @param identifier The identifier of the Spacececraft.
         */
        this.scAdded = function (identifier) {
            $rootScope.$broadcast(this.SC_ADDED_EVENT, identifier);
        };

        /**
         * Function that broadcasts the event associated with the removal of a
         * new Spacececraft.
         * @param identifier The identifier of the Spacececraft.
         */
        this.scRemoved = function (identifier) {
            $rootScope.$broadcast(this.SC_REMOVED_EVENT, identifier);
        };

        /**
         * Function that broadcasts the event associated with the update of
         * new Spacececraft.
         * @param identifier The identifier of the Spacececraft.
         */
        this.scUpdated = function (identifier) {
            $rootScope.$broadcast(this.SC_UPDATED_EVENT, identifier);
        };

    }]);;/**
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
angular.module('satnet-services', ['jsonrpc']);

/**
 * Service that defines the basic calls to the services of the SATNET network
 * through JSON RPC. It defines a common error handler for all the errors that
 * can be overriden by users.
 */
angular.module('satnet-services').service('satnetRPC', [
    'jsonrpc', '$location', '$log', '$q', '$http',
    function (jsonrpc, $location, $log, $q, $http) {
        'use strict';

        var _rpc = $location.protocol() + '://' +
            $location.host() + ':' + $location.port() + '/jrpc/';

        this._configuration = jsonrpc.newService('configuration', _rpc);
        this._simulation = jsonrpc.newService('simulation', _rpc);
        this._leop = jsonrpc.newService('leop', _rpc);

        this._services = {
            // Configuration methods (Ground Stations)
            'gs.list':
                this._configuration.createMethod('gs.list'),
            'gs.add':
                this._configuration.createMethod('gs.create'),
            'gs.get':
                this._configuration.createMethod('gs.getConfiguration'),
            'gs.update':
                this._configuration.createMethod('gs.setConfiguration'),
            'gs.delete':
                this._configuration.createMethod('gs.delete'),
            // Configuration methods (Spacecraft)
            'sc.list':
                this._configuration.createMethod('sc.list'),
            'sc.add':
                this._configuration.createMethod('sc.create'),
            'sc.get':
                this._configuration.createMethod('sc.getConfiguration'),
            'sc.update':
                this._configuration.createMethod('sc.setConfiguration'),
            'sc.delete':
                this._configuration.createMethod('sc.delete'),
            // User configuration
            'user.getLocation':
                this._configuration.createMethod('user.getLocation'),
            // TLE methods
            'tle.celestrak.getSections':
                this._configuration.createMethod('tle.celestrak.getSections'),
            'tle.celestrak.getResource':
                this._configuration.createMethod('tle.celestrak.getResource'),
            'tle.celestrak.getTle':
                this._configuration.createMethod('tle.celestrak.getTle'),
            // Simulation methods
            'sc.getGroundtrack':
                this._simulation.createMethod('spacecraft.getGroundtrack'),
            'sc.getPasses':
                this._simulation.createMethod('spacecraft.getPasses'),
            'gs.getPasses':
                this._simulation.createMethod('groundstation.getPasses'),
            // LEOP services
            'leop.cfg':
                this._leop.createMethod('getConfiguration'),
            'leop.setCfg':
                this._leop.createMethod('setConfiguration'),
            'leop.passes':
                this._leop.createMethod('getPasses'),
            'leop.gs.list':
                this._leop.createMethod('gs.list'),
            'leop.sc.list':
                this._leop.createMethod('sc.list'),
            'leop.gs.add':
                this._leop.createMethod('gs.add'),
            'leop.gs.remove':
                this._leop.createMethod('gs.remove'),
            'leop.ufo.add':
                this._leop.createMethod('launch.addUnknown'),
            'leop.ufo.remove':
                this._leop.createMethod('launch.removeUnknown'),
            'leop.ufo.identify':
                this._leop.createMethod('launch.identify'),
            'leop.ufo.forget':
                this._leop.createMethod('launch.forget'),
            'leop.ufo.update':
                this._leop.createMethod('launch.update'),
            'leop.messages':
                this._leop.createMethod('getMessages')
        };

        /**
         * Method for calling the remote service through JSON-RPC.
         * @param service The name of the service, as per the internal services
         * name definitions.
         * @param params The parameters for the service (as an array).
         * @returns {*}
         */
        this.rCall = function (service, params) {
            if ((this._services.hasOwnProperty(service)) === false) {
                throw '[satnetRPC] service not found, id = <' + service + '>';
            }
            $log.info(
                '[satnetRPC] Invoked service = <' + service + '>' +
                    ', params = ' + JSON.stringify(params)
            );
            return this._services[service](params).then(
                function (data) { return data.data; },
                function (error) {
                    var msg = '[satnetRPC] Error invoking = <' + service +
                        '>, with params = <' + JSON.stringify(params) +
                        '>, description = <' + JSON.stringify(error) + '>';
                    $log.warn(msg);
                    throw error.message
                        .replace(/Exception\('/g, '')
                        .replace(/',\)/g, '');
                }
            );
        };

        /**
         * Retrieves the user location using an available Internet service.
         * @returns Promise that returns a { latitude, longitude } object.
         */
        this.getUserLocation = function () {
            return $http
                .get('/configuration/user/geoip')
                .then(function (data) {
                    $log.info('[satnet] user@(' + JSON.stringify(data.data) + ')');
                    return {
                        latitude: parseFloat(data.data.latitude),
                        longitude: parseFloat(data.data.longitude)
                    };
                });
        };

        /**
         * Retrieves the server location using an available Internet service.
         * @returns Promise that returns a { latitude, longitude } object.
         */
        this.getServerLocation = function (hostname) {
            return $http
                .post('/configuration/hostname/geoip', {'hostname': hostname})
                .then(function (data) {
                    $log.info(
                        '[satnet] server name = ' + hostname +
                            '@(' + JSON.stringify(data.data) + ')'
                    );
                    return {
                        latitude: parseFloat(data.data.latitude),
                        longitude: parseFloat(data.data.longitude)
                    };
                });
        };

        /**
         * Reads the configuration for a given spacecraft, including the
         * estimated groundtrack.
         * @param scId The identifier of the spacecraft.
         * @returns Promise that resturns the Spacecraft configuration object.
         */
        this.readSCCfg = function (scId) {
            var cfg = {},
                p = [
                    this.rCall('sc.get', [scId]),
                    this.rCall('sc.getGroundtrack', [scId]),
                    this.rCall('tle.celestrak.getTle', [scId])
                ];
            return $q.all(p).then(function (results) {
                cfg = results[0];
                cfg.groundtrack = results[1];
                cfg.tle = results[2];
                angular.extend(cfg, results[0]);
                angular.extend(cfg.groundtrack, results[1]);
                angular.extend(cfg.tle, results[2]);
                return cfg;
            });
        };

        /**
         * Reads the configuration for all the GroundStations associated with
         * this LEOP cluster.
         * @param leop_id Identifier of the LEOP cluster.
         * @returns {*} { leop_gs_available: [gs_cfg], leop_gs_inuse: [gs_cfg]}
         */
        this.readAllLEOPGS = function (leop_id) {
            var self = this;
            return this.rCall('leop.gs.list', [leop_id])
                .then(function (gss) {
                    var p = [];
                    angular.forEach(gss.leop_gs_available, function (gs) {
                        p.push(self.rCall('gs.get', [gs]));
                    });
                    angular.forEach(gss.leop_gs_inuse, function (gs) {
                        p.push(self.rCall('gs.get', [gs]));
                    });
                    return $q.all(p).then(function (results) {
                        var a_cfgs = [], u_cfgs = [], j, r_j, r_j_id;
                        for (j = 0; j < results.length; j += 1) {
                            r_j = results[j];
                            r_j_id = r_j.groundstation_id;
                            if (gss.leop_gs_available.indexOf(r_j_id) >= 0) {
                                a_cfgs.push(r_j);
                            } else {
                                u_cfgs.push(r_j);
                            }
                        }
                        return {
                            leop_gs_available: a_cfgs,
                            leop_gs_inuse: u_cfgs
                        };
                    });
                });
        };

    }]);;/**
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
    'satnet-services',
    'leaflet-directive'
]);

angular.module('map-services')
    .constant('T_OPACITY', 0.125)
    .constant('LAT', 37.7833)
    .constant('LNG', -122.4167)
    .constant('MIN_ZOOM', 2)
    .constant('MAX_ZOOM', 12)
    .constant('ZOOM', 7)
    .service('maps', [
        '$q',
        'leafletData',
        'satnetRPC',
        'MIN_ZOOM',
        'MAX_ZOOM',
        'ZOOM',
        'T_OPACITY',
        function (
            $q,
            leafletData,
            satnetRPC,
            MIN_ZOOM,
            MAX_ZOOM,
            ZOOM,
            T_OPACITY
        ) {

            'use strict';

            /**
             * Returns the mapInfo structure for the rest of the chained
             * promises.
             * @returns {*} Promise that returns the mapInfo structure with
             *               a reference to the Leaflet map object.
             */
            this.getMainMap = function () {
                return leafletData.getMap('mainMap').then(function (m) {
                    return { map: m };
                });
            };

            /**
             * Redraws the Terminator to its new position.
             * @returns {*} Promise that returns the updated Terminator object.
             * @private
             */
            this._updateTerminator = function (t) {
                var t2 = L.terminator();
                t.setLatLngs(t2.getLatLngs());
                t.redraw();
                return t;
            };

            /**
             * Creates the main map and adds a terminator for the illuminated
             * surface of the Earth.
             * @returns {*} Promise that returns the mapInfo object
             *               {map, terminator}.
             */
            this._createTerminatorMap = function () {
                var update_function = this._updateTerminator;
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
             * @returns {*} Promise that returns the 'mapData' structure with
             *               a reference to the Leaflet map and to the
             *               terminator overlaying line (if requested).
             */
            this.createMainMap = function (terminator) {

                var p = [];

                if (terminator) {
                    p.push(this._createTerminatorMap());
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
             * Creates a map centered at the estimated user position.
             *
             * @param scope $scope to be configured
             * @param zoom Zoom level
             * @returns {ng.IPromise<{empty}>|*}
             */
            this.autocenterMap = function (scope, zoom) {
                var self = this;
                return satnetRPC.getUserLocation().then(function (location) {
                    self.centerMap(
                        scope,
                        location.latitude,
                        location.longitude,
                        zoom
                    );
                });
            };

            /**
             * Creates a map centered at the position of the given
             * GroundStation.
             *
             * @param scope $scope to be configured
             * @param identifier Identifier of the GroundStation
             * @param zoom Zoom level
             * @returns {ng.IPromise<{}>|*}
             */
            this.centerAtGs = function (scope, identifier, zoom) {
                var self = this;
                return satnetRPC.rCall('gs.get', [identifier])
                    .then(function (cfg) {
                        self.centerMap(
                            scope,
                            cfg.groundstation_latlon[0],
                            cfg.groundstation_latlon[1],
                            zoom
                        );
                        return cfg;
                    });
            };

            /**
             * Configures the given scope variable to correctly hold a map. It
             * zooms with the provided level, at the center given through the
             * latitude and longitude parameters. It also adds a draggable
             * marker at the center of the map.
             *
             * @param scope Scope to be configured (main variables passed as
             *              instances to angular-leaflet should have been
             *              already created, at least, as empty objects before
             *              calling this function)
             * @param latitude Latitude of the map center
             * @param longitude Longitude of the map center
             * @param zoom Zoom level
             */
            this.centerMap = function (scope, latitude, longitude, zoom) {
                angular.extend(
                    scope.center,
                    {
                        lat: latitude,
                        lng: longitude,
                        zoom: zoom
                    }
                );
                angular.extend(scope.markers, {
                    gs: {
                        lat: latitude,
                        lng: longitude,
                        focus: true,
                        draggable: true,
                        label: {
                            message: 'Drag me!',
                            options: {
                                noHide: true
                            }
                        }
                    }
                });
                angular.extend(
                    scope.layers.baselayers,
                    this.getOSMBaseLayer()
                );
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
                        url: 'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',
                        layerOptions: {
                            noWrap: false,
                            continuousWorld: false,
                            minZoom: MIN_ZOOM,
                            maxZoom: MAX_ZOOM,
                            attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ'
                        }
                    },
                    osm_baselayer: {
                        name: 'OSM Base Layer',
                        type: 'xyz',
                        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                        layerOptions: {
                            noWrap: false,
                            continuousWorld: false,
                            minZoom: MIN_ZOOM,
                            maxZoom: MAX_ZOOM,
                            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                        }
                    }
                };
            };

            /**
             * Returns the OSM baselayer for Angular Leaflet.
             *
             * @returns {{osm_baselayer: {name: string, type: string, url: string, layerOptions: {noWrap: boolean, attribution: string}}}}
             */
            this.getOSMBaseLayer = function () {
                return {
                    osm_baselayer: {
                        name: 'OSM Base Layer',
                        type: 'xyz',
                        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                        layerOptions: {
                            noWrap: true,
                            continuousWorld: false,
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
                            continuousWorld: false,
                            minZoom: MIN_ZOOM,
                            maxZoom: MAX_ZOOM,
                            attribution: 'Imagery from <a href="http://giscience.uni-hd.de/">GIScience Research Group @ University of Heidelberg</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                        }
                    },
                    hydda_roads_labels_overlay: {
                        name: 'Roads and Labels',
                        type: 'xyz',
                        url: 'http://{s}.tile.openstreetmap.se/hydda/roads_and_labels/{z}/{x}/{y}.png',
                        layerOptions: {
                            noWrap: true,
                            continuousWorld: false,
                            minZoom: MIN_ZOOM,
                            maxZoom: MAX_ZOOM,
                            attribution: 'Tiles courtesy of <a href="http://openstreetmap.se/" target="_blank">OpenStreetMap Sweden</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                        }
                    },
                    stamen_toner_labels_overlay: {
                        name: 'Labels',
                        type: 'xyz',
                        url: 'http://{s}.tile.stamen.com/toner-labels/{z}/{x}/{y}.png',
                        layerOptions: {
                            noWrap: true,
                            continuousWorld: false,
                            minZoom: MIN_ZOOM,
                            maxZoom: MAX_ZOOM,
                            subdomains: 'abcd',
                            attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                        }
                    },
                    owm_rain_overlay: {
                        name: 'Rain',
                        type: 'xyz',
                        url: 'http://{s}.tile.openweathermap.org/map/rain/{z}/{x}/{y}.png',
                        layerOptions: {
                            noWrap: true,
                            continuousWorld: false,
                            minZoom: MIN_ZOOM,
                            maxZoom: MAX_ZOOM,
                            opacity: 0.325,
                            attribution: 'Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>'
                        }
                    },
                    owm_temperature_overlay: {
                        name: 'Temperature',
                        type: 'xyz',
                        url: 'http://{s}.tile.openweathermap.org/map/temp/{z}/{x}/{y}.png',
                        layerOptions: {
                            noWrap: true,
                            continuousWorld: false,
                            minZoom: MIN_ZOOM,
                            maxZoom: MAX_ZOOM,
                            attribution: 'Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>'
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
    ]);;/**
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
    .constant('_GEOLINE_STEPS', 1)
    .service('markers', [
        '$log', 'maps', '_SIM_DAYS', '_GEOLINE_STEPS',
        function ($log, maps, _SIM_DAYS, _GEOLINE_STEPS) {
            'use strict';

            /******************************************************************/
            /****************************************************** MAP SCOPE */
            /******************************************************************/

            // Structure that holds a reference to the map and to the
            // associated structures.
            this._mapInfo = {};
            // Scope where the leaflet angular pluing has its variables.
            this._mapScope = {};

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

                angular.extend(
                    this._mapScope,
                    {
                        center: {
                            lat: maps.LAT,
                            lng: maps.LNG,
                            zoom: maps.ZOOM
                        },
                        layers: {
                            baselayers: {},
                            overlays: {}
                        },
                        markers: {},
                        paths: {},
                        maxbounds: {}
                    }
                );
                angular.extend(
                    this._mapScope.layers.baselayers,
                    maps.getBaseLayers()
                );
                angular.extend(
                    this._mapScope.layers.overlays,
                    maps.getOverlays()
                );
                angular.extend(
                    this._mapScope.layers.overlays,
                    this.getOverlays()
                );

                var mapInfo = this._mapInfo;
                maps.createMainMap(true).then(function (data) {
                    $log.log(
                        '[map-controller] Created map = <' +
                            maps.asString(data) + '>'
                    );
                    angular.extend(mapInfo, data);
                    return mapInfo;
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
                console.log('gs_id = ' + gs_identifier);
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
             * @returns {{network: {name: string, type: string, visible: boolean}, groundstations: {name: string, type: string, visible: boolean}}}
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
                    // TODO BUG: path removal if added as a layer (angular-leaflet)
                    // layer: 'network',
                    //color: '#A52A2A',
                    color: 'gray',
                    type: 'polyline',
                    weight: 3,
                    opacity: 0.25,
                    latlngs: [s_marker, g_marker],
                    identifier: c_id
                };

                angular.extend(this.getScope().paths, r);
                return c_id;

            };

            /**
             * Pans the current view of the map to the coordinates of the marker
             * for the given groundstation.
             * @param groundstation_id Identifier of the groundstation
             */
            this.panToGSMarker = function (groundstation_id) {

                var marker = this.getMarker(groundstation_id),
                    m_ll = new L.LatLng(marker.lat, marker.lng);

                return maps.getMainMap().then(function (mapInfo) {
                    mapInfo.map.panTo(m_ll, { animate: true });
                    return {
                        latitude: marker.lat,
                        longitude: marker.lng
                    };
                });

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
                var p_key = this.getMarkerKey(
                        this.createConnectorIdentifier(identifier)
                    ),
                    m_key = this.getMarkerKey(identifier);
                delete this.getScope().markers[m_key];
                delete this.getScope().paths[p_key];
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
                    iconSize: [15, 15]
                })
            };

            this.trackStyle = {
                weight: 1,
                opacity: 0.725,
                steps: _GEOLINE_STEPS
            };

            this.colors = [
                //'#57EF1E', '#47DE2D', '#37CD3C', '#27BC4B', '#17AB5A'
                //'#00DFFC', '#00B4CC', '#008C9E', '#005F6B',
                '#00ABAF', '#74FF60', '#499F3C', '#2C6024'
                /*
                '#000033', '#003333', '#006633', '#009933', '#00CC33',
                '#00FF33', '#000066', '#003366', '#006666', '#009966',
                '#00CC66' '#00FF66'
                */
            ];
            this.color_n = 0;

            /**
             * Pans the current view of the map to the coordinates of the marker
             * for the given spacecraft.
             * @param spacecraft_id Identifier of the spacecraft
             */
            this.panToSCMarker = function (spacecraft_id) {

                if (!this.sc.hasOwnProperty(spacecraft_id)) {
                    throw '[markers] Spacecraft does not exist, id = ' +
                        spacecraft_id;
                }

                var sc_marker = this.sc[spacecraft_id],
                    m_ll = sc_marker.marker.getLatLng();

                return maps.getMainMap().then(function (mapInfo) {
                    mapInfo.map.panTo(m_ll, { animate: true });
                    return {
                        lat: m_ll.lat,
                        lng: m_ll.lng
                    };
                });

            };

            /**
             * For a given Spacecraft configuration object, it creates the
             * marker for the spacecraft, its associated label and the
             * groundtrack.
             *
             * @param cfg Configuration object.
             * @returns {{marker: L.Marker, track: L.polyline}}
             */
            this.createSCMarkers = function (cfg) {

                var id = cfg.spacecraft_id,
                    gt,
                    mo = this.scStyle,
                    color =  this.colors[this.color_n % this.colors.length];
                this.color_n += 1;
                this.trackStyle.color = color;
                gt = this.readTrack(cfg.groundtrack);

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
             * Function that reads the RAW groundtrack from the server and
             * transforms it into a usable one for the JS client.
             *
             * @param groundtrack RAW groundtrack from the server.
             * @returns {{durations: Array, positions: Array, geopoints: Array}}
             */
            this.readTrack = function (groundtrack) {

                var i, gt_i,
                    positions = [], durations = [], geopoints = [],
                    first = true,
                    valid = false,
                    t0 = Date.now() * 1000,
                    tf = moment().add(
                        _SIM_DAYS,
                        "days"
                    ).toDate().getTime() * 1000;

                if ((groundtrack === null) || (groundtrack.length === 0)) {
                    throw 'Groundtrack is empty!';
                }

                for (i = 0; i < groundtrack.length; i += 1) {
                    gt_i = groundtrack[i];

                    if (gt_i.timestamp < t0) {
                        continue;
                    }
                    if (gt_i.timestamp > tf) {
                        break;
                    }

                    positions.push([gt_i.latitude, gt_i.longitude]);
                    geopoints.push(new L.LatLng(gt_i.latitude, gt_i.longitude));

                    if (first === true) {
                        first = false;
                        continue;
                    }

                    durations.push(
                        (gt_i.timestamp - groundtrack[i - 1].timestamp) / 1000
                    );
                    valid = true;

                }

                if (valid === false) {
                    throw 'No valid points in the groundtrack';
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
             *              marker: m.L.Marker,
             *              track: m.L
             *          }}
             */
            this.addSC = function (id, cfg) {

                if (this.sc.hasOwnProperty(id)) {
                    throw '[markers] SC Marker already exists, id = ' + id;
                }

                var m = this.createSCMarkers(cfg);
                this.sc[id] = m;
                this.scLayers.addLayer(m.marker);
                this.trackLayers.addLayer(m.track);

                return maps.getMainMap().then(function (mapInfo) {
                    m.track.addTo(mapInfo.map);
                    m.marker.addTo(mapInfo.map);
                    return id;
                });

            };

            /**
             * Updates the configuration for a given Spacecraft object.
             *
             * @param id Identifier of the spacecraft.
             * @param cfg Object with the new configuration for the Spacecraft.
             * @returns {String} Identifier of the just-updated Spacecraft.
             */
            this.updateSC = function (id, cfg) {
                var self = this;
                if (!this.sc.hasOwnProperty(id)) {
                    throw '[markers] SC Marker does not exist! id = ' + id;
                }

                this.removeSC(id).then(function (data) {
                    console.log('[markers] SC removed, id = ' + data);
                    self.addSC(id, cfg).then(function (data) {
                        console.log('[markers] SC added, id = ' + data);
                    });
                });

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
    ]);;/**
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
 * Created by rtubio on 10/28/14.
 */

/** Module definition (empty array is vital!). */
angular.module('x-server-models', ['satnet-services', 'marker-models']);

/**
 * eXtended Server models. Services built on top of the satnetRPC service and
 * the markers models. Right now, there is no need for adding the intermediate
 * bussiness logic with the basic models.
 */
angular.module('x-server-models').service('xserver', [
    '$location', 'satnetRPC',  'markers',
    function ($location, satnetRPC, markers) {

        'use strict';

        this.initStandalone = function () {
            var identifier = $location.host();
            return satnetRPC.getServerLocation(identifier)
                .then(function (data) {
                    return markers.createServerMarker(
                        identifier,
                        data.latitude,
                        data.longitude
                    );
                });
        };

    }
]);;/**
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

/** Module definition . */
angular.module('x-groundstation-models', [
    'pushServices',
    'broadcaster',
    'satnet-services',
    'pushServices',
    'marker-models'
]);

/**
 * eXtended GroundStation models. Services built on top of the satnetRPC
 * service and the basic GroundStation models.
 */
angular.module('x-groundstation-models').service('xgs', [
    '$rootScope', '$q', 'satnetPush', 'broadcaster', 'satnetRPC', 'markers',
    function ($rootScope, $q, satnetPush, broadcaster, satnetRPC, markers) {
        'use strict';

        /**
         * Initializes all the GroundStations reading the information from
         * the server. Markers are indirectly initialized.
         * @returns {ng.IPromise<[String]>} Identifier of the read GS.
         */
        this.initAll = function () {
            var self = this;
            return satnetRPC.rCall('gs.list', []).then(function (gss) {
                return self._initAll(gss);
            });
        };

        /**
         * Initializes all the GroundStations reading the information from
         * the server, for all those that are registered for this LEOP cluster.
         * Markers are indirectly initialized.
         * @returns {ng.IPromise<[String]>} Identifier of the read GS.
         */
        this.initAllLEOP = function (leop_id) {
            var self = this;
            return satnetRPC.rCall('leop.gs.list', [leop_id])
                .then(function (gss) {
                    return self._initAll(gss.leop_gs_inuse);
                });
        };

        /**
         * Common and private method for GroundStation initializers.
         * @param list The list of identifiers of the GroundStation objects.
         * @returns {ng.IPromise<[String]>} Identifier of the read GS.
         * @private
         */
        this._initAll = function (list) {
            var self = this, p = [];
            angular.forEach(list, function (gs) { p.push(self.addGS(gs)); });
            return $q.all(p).then(function (gs_ids) {
                var ids = [];
                angular.forEach(gs_ids, function (id) { ids.push(id); });
                return ids;
            });
        };

        /**
         * Adds a new GroundStation together with its marker, using the
         * configuration object that it retrieves from the server.
         *
         * @param identifier Identififer of the GroundStation to be added.
         * @returns String Identifier of the just-created object.
         */
        this.addGS = function (identifier) {
            return satnetRPC.rCall('gs.get', [identifier]).then(function (data) {
                return markers.createGSMarker(data);
            });
        };

        /**
         * Updates the markers for the given GroundStation object.
         * @param identifier Identifier of the GroundStation object.
         */
        this.updateGS = function (identifier) {
            satnetRPC.rCall('gs.get', [identifier]).then(function (data) {
                return markers.updateGSMarker(data);
            });
        };

        /**
         * Removes the markers for the given GroundStation object.
         * @param identifier Identifier of the GroundStation object.
         */
        this.removeGS = function (identifier) {
            return markers.removeGSMarker(identifier);
        };

        /**
         * Private method that creates the event listeners for this service.
         */
        this.initListeners = function () {
            var self = this;
            $rootScope.$on(broadcaster.GS_ADDED_EVENT, function (event, id) {
                console.log(
                    '@on-gs-added-event, event = ' + event + ', id = ' + id
                );
                self.addGS(id);
            });
            $rootScope.$on(broadcaster.GS_REMOVED_EVENT, function (event, id) {
                console.log(
                    '@on-gs-removed-event, event = ' + event + ', id = ' + id
                );
                self.removeGS(id);
            });
            $rootScope.$on(broadcaster.GS_UPDATED_EVENT, function (event, id) {
                console.log(
                    '@on-gs-updated-event, event = ' + event + ', id = ' + id
                );
                self.updateGS(id);
            });
            satnetPush.bindGSAdded(broadcaster.gsAddedPusher);
            satnetPush.bindGSUpdated(broadcaster.gsUpdatedPusher);
            satnetPush.bindGSRemoved(broadcaster.gsRemovedPusher);
        };

    }
]);;/**
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
 * Created by rtubio on 10/28/14.
 */

/** Module definition (empty array is vital!). */
angular.module('x-spacecraft-models', [
    'broadcaster', 'satnet-services', 'marker-models'
]);

/**
 * eXtended GroundStation models. Services built on top of the satnetRPC
 * service and the basic Spacecraft models.
 */
angular.module('x-spacecraft-models').service('xsc', [
    '$rootScope', '$q', 'broadcaster', 'satnetRPC', 'markers',
    function ($rootScope, $q, broadcaster, satnetRPC, markers) {

        'use strict';

        /**
         * Initializes all the configuration objects for the available
         * spacecraft.
         * @returns {ng.IPromise<[String]>} Identifier of the read SC.
         */
        this.initAll = function () {
            var self = this;
            return satnetRPC.rCall('sc.list', []).then(function (scs) {
                var p = [];
                angular.forEach(scs, function (sc) { p.push(self.addSC(sc)); });
                return $q.all(p).then(function (sc_ids) {
                    return sc_ids;
                });
            });
        };

        /**
         * Initializes all the configuration objects for the available
         * spacecraft.
         * @returns {ng.IPromise<[String]>} Identifier of the read SC.
         */
        this.initAllLEOP = function () {
            var self = this;
            return satnetRPC.rCall('leop.sc.list', [$rootScope.leop_id])
                .then(function (scs) {
                    var p = [];
                    angular.forEach(scs, function (sc) {
                        p.push(self.addSC(sc));
                    });
                    return $q.all(p).then(function (sc_ids) {
                        return sc_ids;
                    });
                });
        };

        /**
         * Adds a new Spacecraft together with its marker, using the
         * configuration object that it retrieves from the server.
         * @param identifier Identififer of the Spacecraft to be added.
         */
        this.addSC = function (identifier) {
            return satnetRPC.readSCCfg(identifier).then(function (data) {
                return markers.addSC(identifier, data);
            });
        };

        /**
         * Updates the configuration for a given Spacecraft.
         * @param identifier The identifier of the Spacecraft.
         */
        this.updateSC = function (identifier) {
            return satnetRPC.readSCCfg(identifier).then(function (data) {
                return markers.updateSC(identifier, data);
            });
        };

        /**
         * Removes the markers for the given Spacecraft.
         * @param identifier The identifier of the Spacecraft.
         */
        this.removeSC = function (identifier) {
            return markers.removeSC(identifier).then(function (data) {
                return data;
            });
        };

        /**
         * Private method that inits the event listeners for this service.
         */
        this.initListeners = function () {
            var self = this;
            $rootScope.$on(broadcaster.SC_ADDED_EVENT, function (event, id) {
                console.log(
                    '@on-sc-added-event, event = ' + event + ', id = ' + id
                );
                self.addSC(id);
            });
            $rootScope.$on(broadcaster.SC_UPDATED_EVENT, function (event, id) {
                console.log(
                    '@on-sc-updated-event, event = ' + event + ', id = ' + id
                );
                self.updateSC(id);
            });
            $rootScope.$on(broadcaster.SC_REMOVED_EVENT, function (event, id) {
                console.log(
                    '@on-sc-removed-event, event = ' + event + ', id = ' + id
                );
                self.removeSC(id);
            });
        };

    }
]);;/**
 * Created by rtubio on 1/13/15.
 */

angular.module('idle', ['ui.bootstrap']);

angular.module('idle')
    .controller('idleCtrl', [
        '$scope', '$modal',
        function ($scope, $modal) {
            'use strict';

            $scope.started = true;

            function closeModals() {
                if ($scope.warning) {
                    $scope.warning.close();
                    $scope.warning = null;
                }

                if ($scope.timedout) {
                    $scope.timedout.close();
                    $scope.timedout = null;
                }
            }

            $scope.$on('$idleStart', function () {
                closeModals();

                $scope.warning = $modal.open({
                    templateUrl: 'idle/warningDialog.html',
                    windowClass: 'modal-danger'
                });

            });

            $scope.$on('$idleEnd', function () {
                closeModals();
            });

            $scope.$on('$idleTimeout', function () {
                closeModals();
                $scope.timedout = $modal.open({
                    templateUrl: 'idle/timedoutDialog.html',
                    windowClass: 'modal-danger'
                });
            });

        }]);;/**
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
    'ui-leop-map-controllers',
    [
        'marker-models',
        'x-spacecraft-models',
        'x-server-models',
        'x-groundstation-models'
    ]
);

angular.module('ui-leop-map-controllers')
    .controller('LEOPMapController', [
        '$rootScope', '$scope', '$log', 'markers', 'xsc', 'xserver', 'xgs',
        function ($rootScope, $scope, $log, markers, xsc, xserver, xgs) {

            'use strict';

            markers.configureMapScope($scope);
            xsc.initListeners();
            xgs.initListeners();

            xsc.initAllLEOP().then(function (spacecraft) {
                $log.log(
                    '[map-controller] Spacecraft =' + JSON.stringify(spacecraft)
                );
            });
            xserver.initStandalone().then(function (server) {
                $log.log(
                    '[map-controller] Server =' + JSON.stringify(server)
                );
                xgs.initAllLEOP($rootScope.leop_id).then(function (gss) {
                    $log.log(
                        '[map-controller] Ground Station(s) = ' +
                            JSON.stringify(gss)
                    );
                });
            });

        }
    ]);
;/**
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
    'ui-leop-menu-controllers',
    [
        'ui.bootstrap',
        'satnet-services',
        'marker-models'
    ]
);

angular.module('ui-leop-menu-controllers').controller('LEOPGSMenuCtrl', [
    '$rootScope', '$scope', '$log', '$modal', 'satnetRPC', 'markers',
    function ($rootScope, $scope, $log, $modal, satnetRPC, markers) {
        'use strict';

        $scope.gsIds = [];

        $scope.panToGS = function (groundstation_id) {
            markers.panToGSMarker(groundstation_id).then(
                function (coordinates) {
                    $log.info(
                        '[menu-gs] Map panned to ' + JSON.stringify(coordinates)
                    );
                }
            );
        };

        $scope.addGroundStation = function () {
            var modalInstance = $modal.open({
                templateUrl: 'templates/leop/manageGroundStations.html',
                controller: 'ManageGSModalCtrl',
                backdrop: 'static',
                size: 'lg'
            });
            console.log('[leop-menu] Created modalInstance = ' + JSON.stringify(modalInstance));
        };
        $scope.refreshGSList = function () {
            satnetRPC.rCall('leop.gs.list', [$rootScope.leop_id])
                .then(function (data) {
                    if ((data !== null) && (data.leop_gs_inuse !== undefined)) {
                        $scope.gsIds = data.leop_gs_inuse.slice(0);
                    }
                });
        };
        $scope.refreshGSList();

    }
]);

angular.module('ui-leop-menu-controllers').controller('clusterMenuCtrl', [
    '$rootScope', '$scope', '$log', '$modal', 'satnetRPC', 'markers',
    function ($rootScope, $scope, $log, $modal, satnetRPC, markers) {
        'use strict';

        $scope.is_anonymous = $rootScope.is_anonymous;
        $scope.ufoIds = [];

        $scope.openManageCluster = function () {
            var modalInstance = $modal.open({
                templateUrl: 'templates/leop/manageCluster.html',
                controller: 'manageClusterModal',
                backdrop: 'static'
            });
            console.log(
                '[leop-menu] Created modalInstance = ' +
                    JSON.stringify(modalInstance)
            );
        };
        $scope.refreshSCList = function () {
            satnetRPC.rCall('leop.sc.list', [$rootScope.leop_id])
                .then(function (data) {
                    if (data !== null) {
                        $scope.scIds = data.slice(0);
                    }
                });
        };
        $scope.panToSC = function (groundstation_id) {
            markers.panToSCMarker(groundstation_id).then(
                function (coordinates) {
                    $log.info(
                        '[menu-gs] Map panned to ' + JSON.stringify(coordinates)
                    );
                }
            );
        };

    }
]);;/**
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
    'ui-leop-modalgs-controllers',
    [ 'broadcaster', 'satnet-services' ]
);

/**
 * Angular module with the Modal GS controllers.
 */
angular.module('ui-leop-modalgs-controllers')
    .controller('ManageGSModalCtrl', [
        '$rootScope',
        '$scope',
        '$modalInstance',
        'broadcaster',
        'satnetRPC',
        function (
            $rootScope,
            $scope,
            $modalInstance,
            broadcaster,
            satnetRPC
        ) {

            'use strict';

            $scope.gsIds = {};
            $scope.gsIds.aItems = [];
            $scope.gsIds.uItems = [];

            $scope.gsIds.toAdd = [];
            $scope.gsIds.toRemove = [];

            $scope.ll_changed = false;

            $scope.init = function () {
                console.log('init, leop_id = ' + $rootScope.leop_id);
                satnetRPC.readAllLEOPGS($rootScope.leop_id)
                    .then(function (data) {
                        console.log('leop.gs.list, data = ' + JSON.stringify(data));
                        if (data === null) { return; }
                        $scope.gsIds = data;
                    });
            };

            $scope.selectGs = function () {
                var i, item;

                if ($scope.gsIds.toAdd === undefined) {
                    $scope.gsIds.toAdd = [];
                }

                for (i = 0; i < $scope.gsIds.aItems.length; i += 1) {
                    item = $scope.gsIds.aItems[i];
                    $scope.gsIds.leop_gs_available.splice(
                        $scope.gsIds.leop_gs_available.indexOf(item),
                        1
                    );
                    if ($scope.gsIds.toAdd.indexOf(item) < 0) {
                        $scope.gsIds.toAdd.push(item);
                    }
                    if ($scope.gsIds.leop_gs_inuse.indexOf(item) < 0) {
                        $scope.gsIds.leop_gs_inuse.push(item);
                    }
                }

                $scope.gsIds.aItems = [];
            };

            $scope.unselectGs = function () {
                var i, item;
                if ($scope.gsIds.toRemove === undefined) {
                    $scope.gsIds.toRemove = [];
                }

                for (i = 0; i < $scope.gsIds.uItems.length; i += 1) {
                    item = $scope.gsIds.uItems[i];
                    $scope.gsIds.leop_gs_inuse.splice(
                        $scope.gsIds.leop_gs_inuse.indexOf(item),
                        1
                    );
                    if ($scope.gsIds.toRemove.indexOf(item) < 0) {
                        $scope.gsIds.toRemove.push(item);
                    }
                    if ($scope.gsIds.leop_gs_available.indexOf(item) < 0) {
                        $scope.gsIds.leop_gs_available.push(item);
                    }
                }

                $scope.gsIds.uItems = [];
            };

            $scope.ok = function () {

                var a_ids = [], r_ids = [], i, gs_id;

                if ($scope.gsIds.toAdd !== undefined) {
                    for (i = 0; i < $scope.gsIds.toAdd.length; i += 1) {
                        gs_id = $scope.gsIds.toAdd[i].groundstation_id;
                        a_ids.push(gs_id);
                        broadcaster.gsAdded(gs_id);
                    }
                    satnetRPC.rCall(
                        'leop.gs.add',
                        [$rootScope.leop_id, a_ids]
                    ).then(
                        function (data) {
                            console.log(
                                '>>> updated LEOP = ' + JSON.stringify(data)
                            );
                        }
                    );
                }

                if ($scope.gsIds.toRemove !== undefined) {
                    for (i = 0; i < $scope.gsIds.toRemove.length; i += 1) {
                        gs_id = $scope.gsIds.toRemove[i].groundstation_id;
                        r_ids.push(gs_id);
                        broadcaster.gsRemoved(gs_id);
                    }
                    satnetRPC.rCall(
                        'leop.gs.remove',
                        [$rootScope.leop_id, r_ids]
                    ).then(
                        function (data) {
                            console.log(
                                '>>> updated LEOP = ' + JSON.stringify(data)
                            );
                        }
                    );
                }

                $modalInstance.close();

            };

            $scope.cancel = function () {
                $modalInstance.close();
            };

            $scope.init();

        }
    ]);;/**
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
angular.module('ui-leop-modalufo-controllers', [
    'ui.bootstrap', 'satnet-services'
]);

angular.module('ui-leop-modalufo-controllers')
    .constant('CLUSTER_CFG_UPDATED_EV', 'cluster-cfg-updated')
    .constant('MAX_OBJECTS', 12)
    .constant('MAX_COLUMNS', 4)
    .service('oArrays', [
        function () {
            'use strict';

            /**
             * Function that checks whether the input parameters represent a
             * proper object array or not.
             * @param array Array for the operation
             * @param property The property for the operation
             */
            this.check = function (array, property) {
                if (!array) {
                    throw 'Array is invalid';
                }
                if (array.length === 0) {
                    return true;
                }
                if (array[0].hasOwnProperty(property) === false) {
                    throw 'Wrong property';
                }
                return true;
            };

            /**
             * Function that searches for the give pair (property, value) within
             * this array of objects.
             * @param array Array for the operation
             * @param property The property for the operation
             * @param value Value that the property equals to
             * @returns {number} Index of the object whose property has the
             *                      desired value
             */
            this.indexOf = function (array, property, value) {
                this.check(array, property);
                var i;
                for (i = 0; i < array.length; i += 1) {
                    if (array[i][property] === value) {
                        return i;
                    }
                }
                throw 'Pair not found in array, = (' +
                    property + ', ' + value + ')';
            };

            /**
             * Function that returns a tuple (index, object) with the object
             * whose property equals to the given value.
             * @param array Array for the operation
             * @param property The property for the operation
             * @param value Value that the property equals to
             * @returns {{index: (number|Number), object: *}}
             */
            this.getObject = function (array, property, value) {
                var index = this.indexOf(array, property, value);
                return {
                    index: index,
                    object: array[index]
                };
            };

            /**
             * Function that returns the tuple (index, value) that has the
             * biggest value within the given array.
             * @param array Array for the operation
             * @param property The property for the operation
             * @returns {{index: number, value: number}}
             */
            this.findMaxTuple = function (array, property) {
                this.check(array, property);

                var i, max_value = -1, max_index = 0;
                for (i = 0; i < array.length; i += 1) {
                    if (array[i][property] > max_value) {
                        max_value = array[i][property];
                        max_index = i;
                    }
                }

                return {
                    index: max_index,
                    value: max_value
                };

            };

            /**
             * Function that returns the same array but changing the strings of
             * the values at the given property by the result of parseInt'ing
             * them.
             * @param array Array for the operation
             * @param property The property for the operation
             * @returns {*}
             */
            this.parseInt = function (array, property) {
                this.check(array, property);
                var i;
                for (i = 0; i < array.length; i += 1) {
                    array[i][property] = parseInt(array[i][property], 10);
                }
                return array;
            };

            /**
             * Splits a given array into a matrix of arrays whose maximum
             * length is the @param max_columms number given as a second
             * parameter.
             * @param array The array to be split
             * @param max_columns Maximum number of columns
             * @returns {*}
             */
            this.split = function (array, max_columns) {

                if (array === null) {
                    throw 'array is null';
                }
                if (max_columns < 1) {
                    throw 'max_columns should be > 1, actual = ' + max_columns;
                }
                if (array === undefined) {
                    return [];
                }
                if (array.length <= max_columns) {
                    return array;
                }

                var i, j, columns, index,
                    rowsNum = Math.ceil(array.length / max_columns),
                    rows = new Array(rowsNum);

                for (i = 0; i < rowsNum; i += 1) {
                    columns = [];
                    for (j = 0; j < max_columns; j += 1) {
                        index = i * max_columns + j;
                        if (index < array.length) {
                            columns[j] = array[index];
                        } else {
                            break;
                        }
                    }
                    rows[i] = columns;
                }

                return rows;

            };

            /**
             * Iterates over the objects of the given array and adds the
             * pair (key, value) to each of those items.
             * @param array Array over wich to iterate
             * @param key Name of the property
             * @param value Value of the property
             * @returns {*}
             */
            this.addProperty = function (array, key, value) {

                if (array === null) {
                    throw 'Array is null';
                }
                if (array.length === 0) {
                    return true;
                }
                if (key === null) {
                    throw 'Key is null';
                }
                if (key.length === 0) {
                    throw 'Key is blank';
                }
                if (value === null) {
                    throw 'Value is null';
                }
                if (array[0].hasOwnProperty(key) === true) {
                    throw 'Property already defined, k = ' + key;
                }
                var i;

                for (i = 0; i < array.length; i += 1) {
                    array[i][key] = value;
                }

                return array;

            };

            /**
             * This function inserts the given element into the array in
             * accordance with the insertion algorithm. The array list is
             * suppossed to be sorted before hand. For the comparison, it
             * uses the <key> property that all the elements of the array
             * should have.
             *
             * @param array Already sorted array
             * @param property Object's property for comparison
             * @param element The element to be inserted
             * @returns {*}
             */
            this.insertSorted = function (array, property, element) {
                this.check(array, property);
                if (element === null) {
                    throw 'Element is null';
                }
                if (element.hasOwnProperty(property) === false) {
                    throw 'Invalid element';
                }
                var i;

                for (i = 0; i < array.length; i += 1) {
                    if (array[i][property] > element[property]) {
                        break;
                    }
                }

                array.splice(i, 0, element);
                return array;

            };

            /**
             * Function that converts an array of objects into a dictionary
             * where the objects can be accessed using as a key the value
             * for their own property. The property chosen is the one whose
             * name was given as a parameter to this function. The property is
             * not erased from the object.
             *
             * @param array Array to be converted
             * @param property Property whose value is used as a key
             * @returns {{}}
             */
            this.array2dict = function (array, property) {
                this.check(array, property);
                if (!property) {
                    throw 'Property is null';
                }
                var obj = {}, dict = {}, key;

                angular.forEach(array, function (i) {
                    angular.extend(obj, i);
                    key = i[property];
                    dict[key] = obj;
                    obj = {};
                });

                return dict;

            };

        }
    ])
    .service('xDicts', [
        function () {
            'use strict';

            /**
             * Function that checks the validity of the parameters passed to
             * most of the functions that this service offers.
             * @param dict The dictionary passed as an argument
             * @param property The property passed as an argument
             * @returns {boolean} 'true' if the operation was succesful
             */
            this.check = function (dict, property) {
                if (!dict) {
                    throw '<Dict> is invalid';
                }
                if (!property) {
                    throw '<property> is invalid';
                }
                return true;
            };

            /**
             * Function that finds the pair key, object of this dictionry whose
             * value for the specified property is the biggest from amongst all
             * in the same dictionary.
             * @param dict The dictionary
             * @param property The property
             * @returns {*[]}
             */
            this.findMaxTuple = function (dict, property) {
                this.check(dict, property);
                var k, max_k, v = 0, max_v = 0, size = 0;
                for (k in dict) {
                    if (dict.hasOwnProperty(k)) {
                        size += 1;
                        v = dict[k][property];
                        if (v < max_v) {
                            continue;
                        }
                        max_v = v;
                        max_k = k;
                    }
                }
                if (size === 0) {
                    return [undefined, 0];
                }
                return [max_k, max_v];
            };

            /**
             * Checks whether this dictionary is empty or not.
             * @param dict The dictionary
             * @returns {boolean} 'true' if the dictionary is empty
             */
            this.isEmpty = function (dict) {
                this.check(dict, 'any');
                var k;
                for (k in dict) {
                    if (dict.hasOwnProperty(k)) {
                        return false;
                    }
                }
                return true;
            };

            /**
             * Returns the length of this dictionary.
             * @param dict The dictionary
             * @returns {number} Length of the dictionary
             */
            this.size = function (dict) {
                this.check(dict, 'any');
                var k, length = 0;
                for (k in dict) {
                    if (dict.hasOwnProperty(k)) {
                        length += 1;
                    }
                }
                return length;
            };

        }
    ])
    .controller('manageClusterModal', [
        '$rootScope', '$scope', '$log', '$modalInstance',
        'broadcaster',
        'satnetRPC', 'oArrays', 'xDicts',
        'MAX_OBJECTS', 'CLUSTER_CFG_UPDATED_EV',
        function (
            $rootScope,
            $scope,
            $log,
            $modalInstance,
            broadcaster,
            satnetRPC,
            oArrays,
            xDicts,
            MAX_OBJECTS,
            CLUSTER_CFG_UPDATED_EV
        ) {
            'use strict';

            $scope.is_anonymous = $rootScope.is_anonymous;
            $scope.cluster = {};

            $scope._init = function (data) {
                $scope.cluster.identifier = data.identifier;
                $scope.cluster.sc_identifier = data.sc_identifier;
                $scope.cluster.old_tle_l1 = data.tle_l1;
                $scope.cluster.old_tle_l2 = data.tle_l2;
                $scope.cluster.tle_l1 = data.tle_l1;
                $scope.cluster.tle_l2 = data.tle_l2;
                $scope.cluster.date = data.date;
                $scope.cluster.max_objects = MAX_OBJECTS;
                $scope.cluster.no_objects = 0;
                $scope.cluster.edit = false;

                oArrays.parseInt(data.ufos, 'object_id');
                $scope.cluster.ufos =
                    $scope._objArr2Dict(data.ufos);
                $scope.cluster.no_ufos = $scope._ufosSize();

                $scope.cluster.editing = {};
                $scope.cluster.no_editing = 0;

                $scope.cluster.identified =
                    $scope._objArr2Dict(data.identified);
                $scope.cluster.no_identified = $scope._identifiedSize();
            };

            $scope._objArr2Dict = function (array) {
                return oArrays.array2dict(array, 'object_id');
            };
            $scope._biggestUfo = function () {
                var array = $scope.cluster.ufos,
                    max = xDicts.findMaxTuple(array, 'object_id');
                return max[1];
            };
            $scope._biggestIded = function () {
                var array = $scope.cluster.identified,
                    max = xDicts.findMaxTuple(array, 'object_id');
                return max[1];
            };
            $scope._nextObjectId = function () {
                var id_ufos = $scope._biggestUfo(),
                    id_identified = $scope._biggestIded();
                return (id_ufos > id_identified)
                    ? parseInt(id_ufos, 10) + 1
                    : parseInt(id_identified, 10) + 1;
            };

            $scope._isUfosEmpty = function () {
                return xDicts.isEmpty($scope.cluster.ufos);
            };
            $scope._ufosSize = function () {
                return xDicts.size($scope.cluster.ufos);
            };
            $scope._addUfo = function (object_id) {
                $scope.cluster.ufos[object_id] = { 'object_id': object_id };
                $scope.cluster.no_ufos += 1;
            };
            $scope._removeUfo = function (object_id) {
                delete $scope.cluster.ufos[object_id];
                $scope.cluster.no_ufos -= 1;
            };
            $scope._getUfo = function (object_id) {
                return $scope.cluster.ufos[object_id];
            };

            $scope._addEditingUfo = function (object_id) {
                if ($scope.is_anonymous) { return; }
                $scope.cluster.editing[object_id] = {
                    object_id: object_id,
                    sc_identifier: '',
                    tle_l1: '',
                    tle_l2: '',
                    callsign: '',
                    edit: true,
                    past: 'ufo'
                };
                $scope.cluster.no_editing += 1;
            };
            $scope._addEditingIded = function (object_id, cfg) {
                $scope.cluster.editing[object_id] = {
                    object_id: object_id,
                    sc_identifier: cfg.sc_id,
                    tle_l1: cfg.tle_l1,
                    tle_l2: cfg.tle_l2,
                    callsign: cfg.callsign,
                    edit: true,
                    past: 'identified'
                };
                $scope.cluster.no_editing += 1;
            };
            $scope._removeEditing = function (object_id) {
                delete $scope.cluster.editing[object_id];
                $scope.cluster.no_editing -= 1;
            };
            $scope._getEditing = function (object_id) {
                return $scope.cluster.editing[object_id];
            };
            $scope._disableEditing = function (object_id) {
                $scope.cluster.editing[object_id].edit = false;
            };

            $scope._identifiedSize = function () {
                return xDicts.size($scope.cluster.identified);
            };
            $scope._addIdentified = function (object_id, cfg) {
                $scope.cluster.identified[object_id] = {
                    object_id: object_id,
                    sc_identifier: cfg.sc_id,
                    tle_l1: cfg.tle_l1,
                    tle_l2: cfg.tle_l2,
                    callsign: cfg.callsign
                };
                $scope.cluster.no_identified += 1;
            };
            $scope._removeIdentified = function (object_id) {
                delete $scope.cluster.identified[object_id];
                $scope.cluster.no_identified -= 1;
            };
            $scope._getIdentified = function (object_id) {
                return $scope.cluster.identified[object_id];
            };

            $scope._updateNoObjects = function () {
                $scope.cluster.no_objects =
                    $scope.cluster.no_ufos +
                    $scope.cluster.no_editing +
                    $scope.cluster.no_identified;
            };

            $scope.init = function () {
                var scope = $scope;
                satnetRPC.rCall('leop.cfg', [$rootScope.leop_id]).then(
                    function (data) {
                        console.log(
                            '[modal-ufo] cluster cfg = ' + JSON.stringify(data)
                        );
                        scope._init(data);
                    }
                );
            };

            $scope.add = function () {
                var next_id = $scope._nextObjectId(), scope = $scope;
                satnetRPC.rCall('leop.ufo.add', [$rootScope.leop_id, next_id])
                    .then(function (data) {
                        $log.info('[modal-ufo] New ufo, id = ' + data);
                        scope._addUfo(next_id);
                    });
            };

            $scope.remove = function () {
                var id = $scope._biggestUfo(), scope = $scope;
                satnetRPC.rCall('leop.ufo.remove', [$rootScope.leop_id, id])
                    .then(function (data) {
                        $log.info('[modal-ufo] Removed ufo, id = ' + data);
                        scope._removeUfo(id);
                    });
            };

            $scope.editingUfo = function (object_id) {
                $scope._addEditingUfo(object_id);
                $scope._removeUfo(object_id);
            };

            $scope.editingIded = function (object_id) {
                if ($scope.is_anonymous) { return; }
                var object = $scope._getIdentified(object_id);
                $scope._addEditingIded(object_id, object);
                $scope._removeIdentified(object_id);
            };

            $scope.cancel = function (object_id) {
                var object = $scope._getEditing(object_id);
                if (object.past === 'ufo') {
                    $scope._addUfo(object_id);
                } else {
                    $scope._addIdentified(object_id, object);
                }
                $scope._removeEditing(object_id);
            };

            $scope.save = function (object_id) {
                var object = $scope._getEditing(object_id);
                $scope._disableEditing(object_id);
                if (object.past === 'ufo') {
                    $scope._saveUfo(object_id, object);
                } else {
                    $scope._saveIded(object_id, object);
                }
            };

            $scope._saveUfo = function (object_id, object) {
                var err_msg = '[modal-ufo] Wrong configuration, ex = ';
                satnetRPC.rCall(
                    'leop.ufo.identify',
                    [
                        $rootScope.leop_id,
                        object_id,
                        object.callsign,
                        object.tle_l1,
                        object.tle_l2
                    ]
                ).then(
                    function (data) {
                        $log.info(
                            '[modal-ufo] <Object#' + data.object_id + '> SAVED!'
                        );
                        object.sc_identifier = data.sc_identifier;
                        $scope._addIdentified(object_id, object);
                        $scope._removeEditing(object_id);
                        broadcaster.scAdded(object.sc_identifier);
                    },
                    function (data) {
                        err_msg += JSON.stringify(data);
                        $log.warn(err_msg);
                        if (alert(err_msg) === false) {
                            $log.warn(err_msg);
                        }
                    }
                );
            };

            $scope._saveIded = function (object_id, object) {
                var err_msg = '[modal-ufo] Wrong configuration, ex = ';
                satnetRPC.rCall(
                    'leop.ufo.update',
                    [
                        $rootScope.leop_id,
                        object_id,
                        object.callsign,
                        object.tle_l1,
                        object.tle_l2
                    ]
                ).then(
                    function (data) {
                        $log.info(
                            '[modal-ufo] <Object#' + data.object_id + '> SAVED!'
                        );
                        object.sc_identifier = data.sc_identifier;
                        $scope._addIdentified(object_id, object);
                        $scope._removeEditing(object_id);
                        broadcaster.scUpdated(object.sc_identifier);
                    },
                    function (data) {
                        err_msg += JSON.stringify(data);
                        $log.warn(err_msg);
                        if (alert(err_msg) === false) {
                            $log.warn(err_msg);
                        }
                    }
                );
            };

            $scope.forget = function (object_id) {
                var ask_msg = 'Are you sure that you want to return <Object#' +
                        object_id + '> back to the UFO list?',
                    err_msg = '[modal-ufo] Wrong configuration, ex = ',
                    object = $scope._getIdentified(object_id),
                    object_sc_id = object.sc_identifier;

                if (confirm(ask_msg) === false) {
                    $log.warn('[modal-ufo] object kept identified.');
                    return;
                }

                satnetRPC.rCall(
                    'leop.ufo.forget',
                    [$rootScope.leop_id, object_id]
                ).then(
                    function (data) {
                        $log.info(
                            '[modal-ufo] <Object#' + data + '> back as a UFO.'
                        );
                        $scope._addUfo(object_id);
                        $scope._removeIdentified(object_id);
                        broadcaster.scRemoved(object_sc_id);
                    },
                    function (data) {
                        err_msg += JSON.stringify(data);
                        $log.warn(err_msg);
                        if (alert(err_msg) === false) {
                            $log.warn(err_msg);
                        }
                    }
                );
            };

            $scope.editCluster = function () {
                $scope.cluster.edit = true;
            };

            $scope.saveCluster = function () {

                var err_msg = '[modal-ufo] Wrong configuration, ex = ',
                    cfg = {
                        identifier: $rootScope.leop_id,
                        date: $scope.cluster.date,
                        tle_l1: $scope.cluster.tle_l1,
                        tle_l2: $scope.cluster.tle_l2
                    };

                satnetRPC.rCall('leop.setCfg', [$rootScope.leop_id, cfg])
                    .then(function (data) {
                        $log.info('[modal-ufo] New cluster cfg, id = ' + data);
                        $scope.cluster.edit = false;
                        $rootScope.$broadcast(CLUSTER_CFG_UPDATED_EV, cfg);
                        broadcaster.scUpdated($scope.cluster.sc_identifier);
                    }, function (data) {
                        err_msg += JSON.stringify(data);
                        $log.warn(err_msg);
                        if (alert(err_msg) === false) {
                            $log.warn(err_msg);
                        }
                    });

            };
            $scope.cancelCluster = function () {
                $scope.cluster.edit = false;
            };

            $scope.hide = function () { $modalInstance.close(); };
            $scope.init();

        }
    ]);;/**
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
        'marker-models',
        'x-groundstation-models',
        'x-spacecraft-models',
        'x-server-models'
    ]
);

angular.module('ui-map-controllers')
    .controller('MapController', [
        '$scope', '$log', 'markers', 'xgs', 'xsc', 'xserver',
        function ($scope, $log, markers, xgs, xsc, xserver) {

            'use strict';

            markers.configureMapScope($scope);
            xgs.initListeners();
            xsc.initListeners();

            xsc.initAll().then(function (spacecraft) {
                $log.log(
                    '[map-controller] Spacecraft =' + JSON.stringify(spacecraft)
                );
            });
            xserver.initStandalone().then(function (server) {
                $log.log(
                    '[map-controller] Server =' + JSON.stringify(server)
                );
                xgs.initAll().then(function (gs_cfgs) {
                    $log.log(
                        '[map-controller] Ground Station(s) = ' +
                            JSON.stringify(gs_cfgs)
                    );
                });
            });

        }
    ]);;/**
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
    'ui-menu-controllers',
    ['ui.bootstrap', 'satnet-services']
);

angular.module('ui-menu-controllers').controller('GSMenuCtrl', [
    '$scope', '$modal', 'satnetRPC',
    function ($scope, $modal, satnetRPC) {

        'use strict';

        $scope.gsIds = [];
        $scope.addGroundStation = function () {
            var modalInstance = $modal.open({
                templateUrl: 'templates/addGroundStation.html',
                controller: 'AddGSModalCtrl',
                backdrop: 'static'
            });
            console.log('Created modalInstance = ' + modalInstance);
        };
        $scope.editGroundStation = function (g) {
            var modalInstance = $modal.open({
                templateUrl: 'templates/editGroundStation.html',
                controller: 'EditGSModalCtrl',
                backdrop: 'static',
                resolve: { groundstationId: function () {
                    return g;
                } }
            });
            console.log('Created modalInstance = ' + modalInstance);
        };
        $scope.refreshGSList = function () {
            satnetRPC.rCall('gs.list', []).then(function (data) {
                if (data !== null) {
                    $scope.gsIds = data.slice(0);
                }
            });
        };
        $scope.refreshGSList();

    }
]);

angular.module('ui-menu-controllers').controller('SCMenuCtrl', [
    '$scope', '$modal', 'satnetRPC',
    function ($scope, $modal, satnetRPC) {

        'use strict';

        $scope.scIds = [];
        $scope.addSpacecraft = function () {
            var modalInstance = $modal.open({
                templateUrl: 'templates/addSpacecraft.html',
                controller: 'AddSCModalCtrl',
                backdrop: 'static'
            });
            console.log('Created modalInstance = ' + modalInstance);
        };
        $scope.editSpacecraft = function (s) {
            var modalInstance = $modal.open({
                templateUrl: 'templates/editSpacecraft.html',
                controller: 'EditSCModalCtrl',
                backdrop: 'static',
                resolve: { spacecraftId: function () {
                    return s;
                } }
            });
            console.log('Created modalInstance = ' + modalInstance);
        };
        $scope.refreshSCList = function () {
            satnetRPC.rCall('sc.list', []).then(function (data) {
                if (data !== null) {
                    console.log('sc.list >>> data = ' + JSON.stringify(data));
                    $scope.scIds = data.slice(0);
                }
            });
        };
        $scope.refreshSCList();

    }
]);

angular.module('ui-menu-controllers').controller('ExitMenuCtrl', [
    '$rootScope', '$scope', '$log',
    function ($rootScope, $scope, $log) {
        'use strict';

        $scope.is_anonymous = $rootScope.is_anonymous;
        $scope.home = function () {
            $log.info('Exiting...');
        };
    }
]);;/**
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
    'ui-modalgs-controllers',
    [
        'ui.bootstrap',
        'nya.bootstrap.select',
        'leaflet-directive',
        'satnet-services',
        'map-services',
        'broadcaster'
    ]
);

angular.module('ui-modalgs-controllers')
    .constant('GS_ELEVATION', 15.0)
    .controller('AddGSModalCtrl', [
        '$scope',
        '$log',
        '$modalInstance',
        'satnetRPC',
        'maps',
        'broadcaster',
        'GS_ELEVATION',
        function (
            $scope,
            $log,
            $modalInstance,
            satnetRPC,
            maps,
            broadcaster,
            GS_ELEVATION
        ) {

            'use strict';

            $scope.gs = {
                identifier: '',
                callsign: '',
                elevation: GS_ELEVATION
            };

            angular.extend($scope, {
                center: {},
                markers: {},
                layers: { baselayers: {}, overlays: {} }
            });

            maps.autocenterMap($scope, 8).then(function () {
                $log.info('[map-ctrl] GS Modal dialog loaded.');
            });

            $scope.ok = function () {
                var newGsCfg = [
                    $scope.gs.identifier,
                    $scope.gs.callsign,
                    $scope.gs.elevation.toFixed(2),
                    $scope.markers.gs.lat.toFixed(6),
                    $scope.markers.gs.lng.toFixed(6)
                ];
                satnetRPC.rCall('gs.add', newGsCfg).then(
                    function (data) {
                        var gsId = data.groundstation_id;
                        $log.info('[map-ctrl] GS added, id = ' + gsId);
                        broadcaster.gsAdded(gsId);
                        $modalInstance.close();
                    },
                    function (error) { window.alert(error); }
                );
            };

            $scope.cancel = function () { $modalInstance.close(); };

        }
    ]);

angular.module('ui-modalgs-controllers')
    .constant('GS_ELEVATION', 15.0)
    .controller('EditGSModalCtrl', [
        '$scope',
        '$log',
        '$modalInstance',
        'satnetRPC',
        'broadcaster',
        'maps',
        'groundstationId',
        function (
            $scope,
            $log,
            $modalInstance,
            satnetRPC,
            broadcaster,
            maps,
            groundstationId
        ) {
            'use strict';

            $scope.gs = { identifier: '', callsign: '', elevation: 0 };

            angular.extend($scope, {
                center: {},
                markers: {},
                layers: { baselayers: {}, overlays: {} }
            });

            maps.centerAtGs($scope, groundstationId, 8).then(function (gs) {
                $scope.gs.identifier = gs.groundstation_id;
                $scope.gs.callsign = gs.groundstation_callsign;
                $scope.gs.elevation = gs.groundstation_elevation;
                $log.info('[map-ctrl] GS Modal dialog loaded.');
            });

            $scope.update = function () {
                var cfg = {
                    'groundstation_id': groundstationId,
                    'groundstation_callsign': $scope.gs.callsign,
                    'groundstation_elevation': $scope.gs.elevation.toFixed(2),
                    'groundstation_latlon': [
                        $scope.markers.gs.lat.toFixed(6),
                        $scope.markers.gs.lng.toFixed(6)
                    ]
                };
                satnetRPC.rCall('gs.update', [groundstationId, cfg]).then(
                    function (data) {
                        $log.info('[map-ctrl] GS updated, id = ' + data);
                        broadcaster.gsUpdated(groundstationId);
                        $modalInstance.close();
                    },
                    function (error) { window.alert(error); }
                );
            };

            $scope.cancel = function () { $modalInstance.close(); };

            $scope.erase = function () {
                if (confirm('Delete this ground station?') === true) {
                    satnetRPC.rCall('gs.delete', [groundstationId]).then(
                        function (gsId) {
                            $log.info(
                                '[modalgs] GS removed, id = ' +
                                    JSON.stringify(gsId)
                            );
                            broadcaster.gsRemoved(gsId);
                            $modalInstance.close();
                        },
                        function (error) { window.alert(error); }
                    );
                }
            };

        }
    ]);;/**
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
    'ui-modalsc-controllers',
    [
        'ui.bootstrap',
        'nya.bootstrap.select',
        'celestrak-services',
        'satnet-services',
        'broadcaster'
    ]
);

angular.module('ui-modalsc-controllers').controller('AddSCModalCtrl', [
    '$scope', '$log', '$modalInstance', 'satnetRPC', 'celestrak', 'broadcaster',
    function ($scope, $log, $modalInstance, satnetRPC, celestrak, broadcaster) {

        'use strict';

        $scope.sc = {
            identifier: '',
            callsign: '',
            tlegroup: '',
            tleid: ''
        };

        $scope.tlegroups = celestrak.CELESTRAK_SELECT_SECTIONS;
        $scope.tles = [];

        $scope.initTles = function (defaultOption) {
            satnetRPC.rCall('tle.celestrak.getResource', [defaultOption])
                .then(function (tleIds) {
                    $scope.tles = tleIds.tle_list.slice(0);
                    console.log('$scope.tles = ' + JSON.stringify($scope.tles));
                });
            $scope.sc.tlegroup = defaultOption;
        };
        $scope.groupChanged = function (value) {
            satnetRPC.rCall('tle.celestrak.getResource', [value.subsection])
                .then(function (tleIds) {
                    $scope.tles = tleIds.tle_list.slice(0);
                });
        };
        $scope.ok = function () {
            var newScCfg = [
                $scope.sc.identifier,
                $scope.sc.callsign,
                $scope.sc.tleid.spacecraft_tle_id
            ];
            satnetRPC.rCall('sc.add', newScCfg).then(function (data) {
                $log.info(
                    '[map-ctrl] SC added, id = ' + data.spacecraft_id
                );
                broadcaster.scAdded(data.spacecraft_id);
            });
            $modalInstance.close();
        };
        $scope.cancel = function () {
            $modalInstance.close();
        };
    }
]);

angular.module('ui-modalsc-controllers').controller('EditSCModalCtrl', [
    '$scope', '$log', '$modalInstance',
    'satnetRPC', 'celestrak', 'spacecraftId', 'broadcaster',
    function ($scope, $log, $modalInstance, satnetRPC, celestrak, spacecraftId, broadcaster) {
        'use strict';

        $scope.sc = {
            identifier: spacecraftId,
            callsign: '',
            tlegroup: '',
            tleid: '',
            savedTleId: ''
        };

        $scope.tlegroups = celestrak.CELESTRAK_SELECT_SECTIONS;
        $scope.tles = [];

        satnetRPC.rCall('sc.get', [spacecraftId]).then(function (data) {
            $scope.sc.identifier = spacecraftId;
            $scope.sc.callsign = data.spacecraft_callsign;
            $scope.sc.savedTleId = data.spacecraft_tle_id;
        });

        $scope.initTles = function (defaultOption) {
            satnetRPC.rCall('tle.celestrak.getResource', [defaultOption])
                .then(function (tleIds) {
                    $scope.tles = tleIds.tle_list.slice(0);
                });
            $scope.sc.tlegroup = defaultOption;
        };

        $scope.groupChanged = function (value) {
            satnetRPC.rCall('tle.celestrak.getResource', [value.subsection])
                .then(function (tleIds) {
                    $scope.tles = tleIds.tle_list.slice(0);
                });
        };
        $scope.update = function () {
            var newScCfg = {
                'spacecraft_id': spacecraftId,
                'spacecraft_callsign': $scope.sc.callsign,
                'spacecraft_tle_id': $scope.sc.tleid.id
            };
            satnetRPC.rCall(
                'sc.update',
                [spacecraftId, newScCfg]
            ).then(function (data) {
                $log.info('[map-ctrl] SC updated, id = ' + data);
                broadcaster.scUpdated(data);
            });
            $modalInstance.close();
        };
        $scope.cancel = function () {
            $modalInstance.close();
        };
        $scope.erase = function () {
            if (confirm('Delete this spacecraft?') === true) {
                satnetRPC.rCall('sc.delete', [spacecraftId]).then(function (data) {
                    $log.info(
                        '[map-ctrl] Spacecraft removed, id = ' +
                            JSON.stringify(data)
                    );
                    broadcaster.scRemoved(data);
                });
                $modalInstance.close();
            }
        };

    }
]);;/*
   Copyright 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

angular.module('countdownDirective', [ 'satnet-services' ])
    .constant('COUNTDOWN_END_EV', 'launch-countdown-end')
    .controller('countdownCtrl', [
        '$rootScope', '$log', '$scope', '$timeout', 'satnetRPC',
        function ($rootScope, $log, $scope, $timeout, satnetRPC) {
            'use strict';

            $scope.cd = {
                label: 'EXPIRED',
                diff: '',
                expired: false,
                hide: false,
                _launch: {},
                _diff: {},
                _timer: {}
            };

            $scope._endBeat = function () {
                $rootScope.$broadcast('launch-countdown-end');
                $timeout.cancel($scope._timer);
                $scope.cd.expired = true;
            };

            $scope.toggle = function () {
                $scope.cd.hide = !$scope.cd.hide;
            };

            $scope.beat = function () {
                $scope.cd._timer = $timeout(function () {

                    var now = moment().utc();

                    if (($scope.cd._launch.isBefore(now) === true) ||
                            ($scope.cd._launch.isSame(now) === true)) {
                        $scope._endBeat();
                        return;
                    }

                    $scope.cd._diff = moment.duration(
                        $scope.cd._launch.diff(now)
                    );
                    $scope.cd.diff = $scope.cd._diff.toISOString();
                    $scope.beat();

                }, 990);
            };

            $scope._init = function (cfg) {
                var now = moment().utc();
                $scope.cd._launch = moment(cfg.date);
                $scope.cd._diff = moment.duration($scope.cd._launch.diff(now));
                $scope.beat();
            };

            $scope.init = function () {
                satnetRPC.rCall('leop.cfg', [$rootScope.leop_id]).then(
                    function (cfg) { $scope._init(cfg); }
                );
                $scope.$on('cluster-cfg-updated', function (id, cfg) {
                    console.log('EVENT, id = ' + id);
                    $log.info('@countdown: updating cluster, cfg = ' + cfg);
                    $scope._init(cfg);
                });
            };

            $scope.init();

        }
    ])
    .filter('cdDate', function () {
        'use strict';

        return function (input) {

            return input.replace(/P/, '').replace(/S/, '')
                        .replace(/DT/, ' days ')
                        .replace(/H/, ':').replace(/M/, ':').replace(/T/, '')
                        .replace(/\.[0-9]{1,}/, '');

        };

    })
    .directive('countdown', function () {
        'use strict';

        return {
            restrict: 'E',
            templateUrl: 'templates/countdown/countdown.html'
        };

    });;/*
   Copyright 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

angular.module('messagesDirective', [
    'satnet-services', 'pushServices', 'ui-leop-modalufo-controllers'
])
    .constant('MAX_MESSAGES', 20)
    .controller('messagesCtrl', [
        '$rootScope', '$scope',
        'satnetRPC', 'satnetPush', 'oArrays', 'MAX_MESSAGES',
        function (
            $rootScope,
            $scope,
            satnetRPC,
            satnetPush,
            oArrays,
            MAX_MESSAGES
        ) {
            'use strict';

            $scope.data = [];

            /**
             * This function pushes a new element into the array using the
             * insertion algorithm and keeping the array sorted by timestamp. It
             * respects the maximum messages limit for the array, as established
             * by the related constant.
             * @param message Message to be inserted within the array
             * @private
             */
            $scope._pushMessage = function (message) {
                if ($scope.data.length === MAX_MESSAGES) {
                    $scope.data.splice(0, 1);
                }
                console.log(
                    '[messages] Message pushed, message = ' +
                        JSON.stringify(message)
                );
                oArrays.insertSorted($scope.data, 'timestamp', message);
            };

            /**
             * Inserts into the data messages array all the messages from the
             * provided array. It uses the insertion algorithm driven by the
             * timestamp field and respects the limit for the maximum number of
             * messages.
             * @param messages Messages array
             * @private
             */
            $scope._pushMessages = function (messages) {
                var date, ts_in_ms;
                angular.forEach(messages, function (m) {
                    ts_in_ms = parseInt(m.timestamp, 10) / 1000;
                    date = new Date(ts_in_ms);
                    m.timestamp = date;
                    $scope._pushMessage(m);
                });
            };

            /**
             * Initializes this controller.
             */
            $scope.init = function () {

                var now = moment().utc(),
                    yesterday = now.subtract(7, 'days');

                satnetRPC.rCall(
                    'leop.messages',
                    [$rootScope.leop_id, yesterday]
                )
                    .then(function (data) {
                        $scope._pushMessages(data);
                        console.log(
                            '[@messagesCtrl.init(), $scope.data = ' +
                                JSON.stringify($scope.data)
                        );
                    });

                satnetPush.bindFrameReceived($scope._pushMessage);

            };

            $scope.init();

        }
    ])
    .directive('messages', function () {
        'use strict';

        return {
            restrict: 'E',
            templateUrl: 'templates/messages/messages.html'
        };

    });;/*
   Copyright 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

angular.module('logNotifierDirective', [])
    .constant('TIMESTAMP_FORMAT', 'HH:mm:ss.sss')
    .controller('logNotifierCtrl', [
        '$scope', '$filter', 'TIMESTAMP_FORMAT',
        function ($scope, $filter, TIMESTAMP_FORMAT) {
            'use strict';

            $scope.eventLog = [];
            $scope.logEvent = function (event, message) {
                $scope.eventLog.unshift({
                    type: event.name,
                    timestamp: $filter('date')(new Date(), TIMESTAMP_FORMAT),
                    msg:  message
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
            $scope.$on('debEvent', function (event, message) {
                $scope.logEvent(event, message);
            });

        }
    ])
    .directive('logNotifier', function () {
        'use strict';

        return {
            restrict: 'E',
            templateUrl: 'templates/notifier/logNotifier.html'
        };

    });;/*
   Copyright 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

angular.module('passDirective', [
    'satnet-services', 'ui-leop-modalufo-controllers'
])
    .service('passSlotsService', [
        '$rootScope', 'satnetRPC', 'oArrays',
        function ($rootScope, satnetRPC, oArrays) {
            'use strict';

            this._generateRowName = function (slot) {
                return slot.gs_identifier + ' / ' + slot.sc_identifier;
            };

            /**
             * Creates a Gantt-like slot object from the slot read from the
             * server.
             * @param slot Slot as read from the server.
             * @returns {{
             *      name: (cfg.groundstation_id|*),
             *      tasks: {name: (cfg.spacecraft_id|*), start: *, end: *}[]
             *  }}
             * @private
             */
            this._createSlot = function (slot) {
                return {
                    name: this._generateRowName(slot),
                    classes: 'my-gantt-row',
                    tasks: [{
                        name: slot.sc_identifier,
                        classes: 'my-gantt-cell',
                        from: new Date(slot.slot_start),
                        to: new Date(slot.slot_end)
                    }]
                };
            };

            /**
             * This function transforms the plain raw format of the server into
             * the one needed by the Gantt chart used within this directive.
             * @param pass_slots Raw passes from the server.
             * @private
             */
            this._parseSlots = function (pass_slots) {

                if (!pass_slots) { throw "<pass_slots> is null"; }

                var gantt_slots = [], g_slot, new_slot, self = this;

                angular.forEach(pass_slots, function (slot) {

                    new_slot = self._createSlot(slot);

                    try {
                        g_slot = oArrays.getObject(
                            gantt_slots,
                            'name',
                            self._generateRowName(slot)
                        ).object;
                        g_slot.tasks.push(new_slot.tasks[0]);
                    } catch (err) {
                        gantt_slots.push(new_slot);
                    }

                });

                return gantt_slots;

            };

            /**
             * Retrieves the slots from the server and transforms them into the
             * format required for the Gantt chart component.
             * @returns {ng.IPromise<>|*}
             */
            this.getPasses = function () {
                var self = this;
                return satnetRPC.rCall('leop.passes', [$rootScope.leop_id])
                    .then(function (passes) {
                        return self._parseSlots(passes);
                    });
            };

        }
    ])
    .controller('passSlotsCtrl', [
        '$scope', 'passSlotsService',
        function ($scope, passSlotsService) {
            'use strict';

            $scope.data = [];
            $scope.init = function () {
                passSlotsService.getPasses().then(function (g_slots) {
                    angular.extend($scope.data, g_slots);
                });
            };

            $scope.init();

        }
    ])
    .directive('passes', function () {
        'use strict';

        return {
            restrict: 'E',
            templateUrl: 'templates/passes/passes.html'
        };

    });;/**
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

/**
 * Main application for the norminal operational phase.
 * @type {ng.IModule}
 */
var app = angular.module('satnet-ui', [
    // AngularJS libraries
    'pushServices',
    'jsonrpc',
    'ngCookies',
    'ngResource',
    'leaflet-directive',
    'remoteValidation',
    'nya.bootstrap.select',
    'ngIdle',
    'pusher-angular',
    // level 1 services/models
    'broadcaster',
    'map-services',
    'celestrak-services',
    'satnet-services',
    // level 2 services/models
    'marker-models',
    // level 3 services/models
    'x-server-models',
    'x-spacecraft-models',
    'x-groundstation-models',
    // level 4 (controllers),
    'ui-map-controllers',
    'ui-menu-controllers',
    'ui-modalsc-controllers',
    'ui-modalgs-controllers',
    'idle',
    // directives
    'logNotifierDirective'
]);

// level 1 services
angular.module('pushServices');
angular.module('broadcaster');
angular.module('map-services');
angular.module('satnet-services');
angular.module('celestrak-services');
// level 2 services
angular.module('marker-models');
// level 3 services
angular.module('x-server-models');
angular.module('x-spacecraft-models');
angular.module('x-groundstation-models');
// level 4 controllers
angular.module('ui-map-controllers');
angular.module('ui-menu-controllers');
angular.module('ui-modalsc-controllers');
angular.module('ui-modalgs-controllers');
// level 5 (directives)
angular.module('logNotifierDirective');

/**
 * Configuration of the main AngularJS logger so that it broadcasts all logging
 * messages as events that can be catched by other visualization UI controllers.
 */
app.config([
    '$keepaliveProvider', '$idleProvider', '$provide',
    function ($keepaliveProvider, $idleProvider, $provide) {
        'use strict';

        $idleProvider.idleDuration(5);
        $idleProvider.warningDuration(5);
        $keepaliveProvider.interval(10);

        $provide.decorator('$log', function ($delegate) {
            var rScope = null;
            return {
                setScope: function (scope) { rScope = scope; },
                log: function (args) {
                    console.log('@log event');
                    $delegate.log.apply(null, ['[log] ' + args]);
                    rScope.$broadcast('logEvent', args);
                },
                info: function (args) {
                    console.log('@info event');
                    $delegate.info.apply(null, ['[info] ' + args]);
                    rScope.$broadcast('infoEvent', args);
                },
                error: function () {
                    console.log('@error event');
                    $delegate.error.apply(null, arguments);
                    rScope.$broadcast('errEvent', arguments);
                },
                warn: function (args) {
                    console.log('@warn event');
                    $delegate.warn.apply(null, ['[warn] ' + args]);
                    rScope.$broadcast('warnEvent', args);
                }
            };
        });

    }
]);

/**
 * Main run method for the AngularJS app.
 */
app.run([
    '$rootScope', '$log', '$http', '$cookies', '$idle',
    function ($rootScope, $log, $http, $cookies, $idle) {
        'use strict';

        $log.setScope($rootScope);
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        $idle.watch();

    }
]);;/**
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

/**
 * Main application for the LEOP operational phase.
 * @type {ng.IModule}
 */
var app = angular.module('leop-ui', [
    // AngularJS libraries
    'jsonrpc',
    'ngCookies',
    'ngResource',
    'leaflet-directive',
    'remoteValidation',
    'angular-loading-bar',
    'ui.bootstrap.datetimepicker',
    'gantt',
    'gantt.labels',
    'gantt.movable',
    'gantt.tooltips',
    'pusher-angular',
    // level 1 services
    'pushServices',
    'broadcaster',
    'map-services',
    'celestrak-services',
    'satnet-services',
    // level 2 services/models
    'marker-models',
    // level 3 services/models
    'x-server-models',
    'x-spacecraft-models',
    'x-groundstation-models',
    // level 4 (controllers),
    'ui-leop-map-controllers',
    'ui-menu-controllers',
    'ui-leop-menu-controllers',
    'ui-leop-modalufo-controllers',
    'ui-leop-modalgs-controllers',
    // directives
    'logNotifierDirective',
    'countdownDirective',
    'passDirective',
    'messagesDirective'
]);

// level 1 services
angular.module('pushServices');
angular.module('broadcaster');
angular.module('map-services');
angular.module('celestrak-services');
angular.module('satnet-services');
// level 2 services (bussiness logic layer)
angular.module('marker-models');
// level 3 services
angular.module('x-server-models');
angular.module('x-spacecraft-models');
angular.module('x-groundstation-models');
// level 4 controllers
angular.module('ui-leop-map-controllers');
angular.module('ui-menu-controllers');
angular.module('ui-leop-menu-controllers');
angular.module('ui-leop-modalufo-controllers');
angular.module('ui-leop-modalgs-controllers');
// level 5 (directives)
angular.module('logNotifierDirective');
angular.module('countdownDirective');
angular.module('passDirective');
angular.module('messagesDirective');

/**
 * Configuration of the main AngularJS logger so that it broadcasts all logging
 * messages as events that can be catched by other visualization UI controllers.
 */
app.config([
    '$provide',
    function ($provide) {
        'use strict';

        $provide.decorator('$log', function ($delegate) {
            var rScope = null;
            return {
                setScope: function (scope) { rScope = scope; },
                log: function (args) {
                    console.log('@log event');
                    $delegate.log.apply(null, ['[log] ' + args]);
                    rScope.$broadcast('logEvent', args);
                },
                info: function (args) {
                    console.log('@info event');
                    $delegate.info.apply(null, ['[info] ' + args]);
                    rScope.$broadcast('infoEvent', args);
                },
                error: function () {
                    console.log('@error event');
                    $delegate.error.apply(null, arguments);
                    rScope.$broadcast('errEvent', arguments);
                },
                warn: function (args) {
                    console.log('@warn event');
                    $delegate.warn.apply(null, ['[warn] ' + args]);
                    rScope.$broadcast('warnEvent', args);
                }
            };
        });

    }
]);

/**
 * Main run method for the AngularJS app.
 */
app.run([
    '$rootScope', '$log', '$http', '$cookies', '$window',
    function ($rootScope, $log, $http, $cookies, $window) {
        'use strict';

        $log.setScope($rootScope);
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        $rootScope.leop_id = $window.leop_id;
        $rootScope.is_anonymous = ($window.is_anonymous === 'True');

    }
]);