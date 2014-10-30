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
angular.module('broadcaster', []);

/**
 * Service used for broadcasting UI events in between controllers.
 */
angular.module('broadcaster')
    .service('broadcaster', [ '$rootScope', function ($rootScope) {

        'use strict';
        
        /**
         * @type {string} Identifier of the event.
         */
        this.GS_ADDED_EVENT = 'gs.added';
        /**
         * @type {string} Identifier of the event.
         */
        this.GS_REMOVED_EVENT = 'gs.removed';
        /**
         * @type {string} Identifier of the event.
         */
        this.GS_UPDATED_EVENT = 'gs.updated';

        /**
         * Function that broadcasts the event associated with the creation of a 
         * new GroundStation.
         * @param gs_id The identifier of the GroundStation.
         */
        this.gsAdded = function (gs_id) {
            $rootScope.$broadcast(this.GS_ADDED_EVENT, gs_id);
        };

        /**
         * Function that broadcasts the event associated with the removal of a 
         * new GroundStation.
         * @param gs_id The identifier of the GroundStation.
         */
        this.gsRemoved = function (gs_id) {
            $rootScope.$broadcast(this.GS_REMOVED_EVENT, gs_id);
        };

        /**
         * Function that broadcasts the event associated with the update of 
         * new GroundStation.
         * @param gs_id The identifier of the GroundStation.
         */
        this.gsUpdated = function (gs_id) {
            $rootScope.$broadcast(this.GS_UPDATED_EVENT, gs_id);
        };

    }]);