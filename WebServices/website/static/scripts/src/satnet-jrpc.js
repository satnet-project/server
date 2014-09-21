/**
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

__JRPC_BASE_URL = 'jrpc/';

/**
 * @constructor
 */
function SatnetJRPC() {
    this.client = new $.JsonRpcClient({
        ajaxUrl: __JRPC_BASE_URL,
        headers: {
            'X-CSRF-Token': $('meta[name="csrf-token"]').attr('content')
        }
    });
}

/**
 * Private handler for the errors during the invokation of the remote methods.
 * @private
 */
SatnetJRPC.prototype.__errorCb = function() {
    console.error('JRPC communication error.');
};

/**
 * Private method for easing the call to the library function. Includes logging
 * and a common error callback handler for the JRPC call.
 * @param method The remote method to be executed.
 * @param parameters The list of parameters for the remote method call.
 * @param successCb The callback function to be executed after a successful
 *                  invokation of the remote method.
 * @returns {*} All the results as returned from the JRPC method.
 * @private
 */
SatnetJRPC.prototype.__jrpc = function(method, parameters, successCb) {
    return this.client.call(
        method, parameters, successCb, this.__errorCb
    );
};

/**
 * JRPC method that gets the list of GroundStations for the user that is
 * currently logged in.
 */
SatnetJRPC.prototype.get_gs_list = function(results_cb) {
    console.log('>>> [jrpc] invoking: configuration.gs.list');
    this.__jrpc('configuration.gs.list', [], results_cb);
};