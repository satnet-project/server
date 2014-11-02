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
angular.module('satnet-services', []);

/**
 * Service that defines the basic calls to the services of the SATNET network
 * through JSON RPC. It defines a common error handler for all the errors that
 * can be overriden by users.
 */
angular.module('satnet-services').service('satnetRPC', [
    'jsonrpc', '$location', '$log', function(jsonrpc, $location, $log) {

    'use strict';

    var rpc = '' +
        $location.protocol() + '://' +
        $location.host() + ':' + $location.port() +
        '/jrpc/';
    this._CfgService = jsonrpc.newService('configuration', rpc);
    this._services = {
        // Configuration methods (Ground Stations)
        'gs.list': this._CfgService.createMethod('gs.list'),
        'gs.add': this._CfgService.createMethod('gs.create'),
        'gs.get': this._CfgService.createMethod('gs.getConfiguration'),
        'gs.update': this._CfgService.createMethod('gs.setConfiguration'),
        'gs.delete': this._CfgService.createMethod('gs.delete'),
         // Configuration methods (Spacecraft)
        'sc.list': this._CfgService.createMethod('sc.list'),
        'sc.add': this._CfgService.createMethod('sc.create'),
        'sc.get': this._CfgService.createMethod('sc.getConfiguration'),
        'sc.update': this._CfgService.createMethod('sc.setConfiguration'),
        'sc.delete': this._CfgService.createMethod('sc.delete')
    };

    /**
     * Common error handler for all the JSON-RPC invocations.
     * @param data The data that defines the error.
     * @private
     */
    this._errorCb = function(data) {
        $log.warn(
            '[satnet-jrpc] Error calling \"satnetRPC\" = ' +
            JSON.stringify(data)
        );
    };

    /**
     * Method for calling the remote service through JSON-RPC.
     * @param service The name of the service, as per the internal services
     *                  name definitions.
     * @param paramArray The parameters for the service (as an array).
     * @param successCb Callback called after a successful remote service
     *                  invokation.
     * @param errorCb Callback called after an error during the remote
     *                  invokation of the service.
     * @deprecated
     */
    this.call = function (service, paramArray, successCb, errorCb) {
        if ( ( service in this._services ) === false ) {
            throw '\"satnetRPC\" service not found, id = ' + service;
        }
        if ( errorCb === null ) { errorCb = this._errorCb; }
        this._services[service](paramArray).success(successCb).error(errorCb);
    };

    /**
     * Method for calling the remote service through JSON-RPC.
     * @param service The name of the service, as per the internal services
     *                  name definitions.
     * @param paramArray The parameters for the service (as an array).
     * @returns {*}
     */
    this.rCall = function(service, paramArray) {
        if ( ( service in this._services ) === false ) {
            throw '\"satnetRPC\" service not found, id = ' + service;
        }
        return this._services[service](paramArray).then(function(data) {
            return data;
        });
    };

}]);