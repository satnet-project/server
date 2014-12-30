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
]);