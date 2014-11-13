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
angular.module('broadcaster').service('broadcaster', [
    '$rootScope',
    function ($rootScope) {

        'use strict';

        this.GS_ADDED_EVENT = 'gs.added';
        this.GS_REMOVED_EVENT = 'gs.removed';
        this.GS_UPDATED_EVENT = 'gs.updated';

        /**
         * Function that broadcasts the event associated with the creation of a
         * new GroundStation.
         * @param gsId The identifier of the GroundStation.
         */
        this.gsAdded = function (gsId) {
            $rootScope.$broadcast(this.GS_ADDED_EVENT, gsId);
        };

        /**
         * Function that broadcasts the event associated with the removal of a
         * new GroundStation.
         * @param gsId The identifier of the GroundStation.
         */
        this.gsRemoved = function (gsId) {
            $rootScope.$broadcast(this.GS_REMOVED_EVENT, gsId);
        };

        /**
         * Function that broadcasts the event associated with the update of
         * new GroundStation.
         * @param gsId The identifier of the GroundStation.
         */
        this.gsUpdated = function (gsId) {
            $rootScope.$broadcast(this.GS_UPDATED_EVENT, gsId);
        };

        this.SC_ADDED_EVENT = 'sc.added';
        this.SC_REMOVED_EVENT = 'sc.removed';
        this.SC_UPDATED_EVENT = 'sc.updated';

        /**
         * Function that broadcasts the event associated with the creation of a
         * new Spacececraft.
         * @param scId The identifier of the Spacececraft.
         */
        this.scAdded = function (scId) {
            $rootScope.$broadcast(this.SC_ADDED_EVENT, scId);
        };

        /**
         * Function that broadcasts the event associated with the removal of a
         * new Spacececraft.
         * @param scId The identifier of the Spacececraft.
         */
        this.scRemoved = function (scId) {
            $rootScope.$broadcast(this.SC_REMOVED_EVENT, scId);
        };

        /**
         * Function that broadcasts the event associated with the update of
         * new Spacececraft.
         * @param scId The identifier of the Spacececraft.
         */
        this.scUpdated = function (scId) {
            $rootScope.$broadcast(this.SC_UPDATED_EVENT, scId);
        };

    }
]);