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
            $location.host() + ':' + $location.port() +
            '/jrpc/';

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
            // LEOP services
            'leop.gs.list':
                this._leop.createMethod('gs.list'),
            'leop.gs.add':
                this._leop.createMethod('gs.add'),
            'leop.gs.remove':
                this._leop.createMethod('gs.remove'),
            'leop.sc.cluster':
                this._leop.createMethod('sc.cluster')
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
                .then(function (data) { return data.data; });
        };

        /**
         * Retrieves the server location using an available Internet service.
         * @returns Promise that returns a { latitude, longitude } object.
         */
        this.getServerLocation = function (hostname) {
            return $http
                .post('/configuration/hostname/geoip', {'hostname': hostname})
                .then(function (data) { return data.data; });
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

    }]);