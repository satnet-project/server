/**
 * Copyright 2014, 2014 Ricardo Tubio-Pardavila
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
 * Created by rtubio on 1/31/14.
 */

/**
 * Basic Simulator's constructor.
 * @constructor
 */
function Simulator($log, listGroundStations) {

    this._log = $log;
    this._listGroundStations = listGroundStations;

    this._loadData();

}

/**
 * Private method that loads the data required by the Simulator from a remote
 * server.
 * @private
 */
Simulator.prototype._loadData = function () {

    this._log.info('[simulator] Loading remote data...');

    this._gs_list = this._listGroundStations.query();
    this._log.info(
            '[simulator] Ground Stations registered = ' + this._gs_list.length
    );

};