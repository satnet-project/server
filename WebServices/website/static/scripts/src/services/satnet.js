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
angular.module('satnet-services', [ 'celestrak-services' ]);

/**
 * Service that defines the basic calls to the services of the SATNET network
 * through JSON RPC. It defines a common error handler for all the errors that
 * can be overriden by users.
 */
angular.module('satnet-services').service('satnetRPC', [
    'jsonrpc', '$location', '$log', '$q', '$http',
    function (jsonrpc, $location, $log, $q, $http) {
        'use strict';

        var rpc = $location.protocol() + '://' +
            $location.host() + ':' + $location.port() +
            '/jrpc/';

        this.configuration = jsonrpc.newService('configuration', rpc);
        this.simulation = jsonrpc.newService('simulation', rpc);
        this.leop = jsonrpc.newService('leop', rpc);

        this.services = {
            // Configuration methods (Ground Stations)
            'gs.list':
                this.configuration.createMethod('gs.list'),
            'gs.add':
                this.configuration.createMethod('gs.create'),
            'gs.get':
                this.configuration.createMethod('gs.getConfiguration'),
            'gs.update':
                this.configuration.createMethod('gs.setConfiguration'),
            'gs.delete':
                this.configuration.createMethod('gs.delete'),
            // Configuration methods (Spacecraft)
            'sc.list':
                this.configuration.createMethod('sc.list'),
            'sc.add':
                this.configuration.createMethod('sc.create'),
            'sc.get':
                this.configuration.createMethod('sc.getConfiguration'),
            'sc.update':
                this.configuration.createMethod('sc.setConfiguration'),
            'sc.delete':
                this.configuration.createMethod('sc.delete'),
            // User configuration
            'user.getLocation':
                this.configuration.createMethod('user.getLocation'),
            // TLE methods
            'tle.celestrak.getSections':
                this.configuration.createMethod('tle.celestrak.getSections'),
            'tle.celestrak.getResource':
                this.configuration.createMethod('tle.celestrak.getResource'),
            'tle.celestrak.getTle':
                this.configuration.createMethod('tle.celestrak.getTle'),
            // Simulation methods
            'sc.getGroundtrack':
                this.simulation.createMethod('spacecraft.getGroundtrack'),
            // LEOP services
            'leop.gs.list':
                this.leop.createMethod('gs.list'),
            'leop.gs.add':
                this.leop.createMethod('gs.add'),
            'leop.gs.remove':
                this.leop.createMethod('gs.remove')
        };

        /**
         * Method for calling the remote service through JSON-RPC.
         * @param service The name of the service, as per the internal services
         * name definitions.
         * @param paramArray The parameters for the service (as an array).
         * @returns {*}
         */
        this.rCall = function (service, paramArray) {
            if ((this.services.hasOwnProperty(service)) === false) {
                throw '[satnetRPC] service not found, id = <' + service + '>';
            }
            $log.log('[satnetRPC] Invoked service = <' + service + '>');
            return this.services[service](paramArray).then(
                function (data) {
                    return data.data;
                },
                function (error) {
                    var msg = '[satnetRPC] Error invoking = <'
                        + service + '>'
                        + ', description = <' + error + '>';
                    $log.warn(msg);
                }
            );
        };

        /**
         * Retrieves the user location using an available Internet service.
         * @returns Promise that returns a { lat, lng } object.
         */
        this.getUserLocation = function () {
            return $http.get('/configuration/user/geoip').then(function (data) {
                return data.data;
            });
        };

        /**
         * Reads the configuration for a given spacecraft, including the
         * estimated groundtrack.
         * @param scId The identifier of the spacecraft.
         * @returns Promise that resturns the Spacecraft configuration object.
         */
        this.readSCCfg = function (scId) {
            var cfg = null,
                p = [
                    this.rCall('sc.get', [scId]),
                    this.rCall('sc.getGroundtrack', [scId]),
                    this.rCall('tle.celestrak.getTle', [scId])
                ];
            return $q.all(p).then(function (results) {
                cfg = results[0];
                cfg.id = results[0].spacecraft_id;
                cfg.groundtrack = results[1];
                cfg.tle = results[2];
                return cfg;
            });
        };

    }]);