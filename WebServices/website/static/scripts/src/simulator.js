/*
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

/**
 * @constructor
 */
function Simulator() {
    this.map = null;
    this.jrpc = new SatnetJRPC();
    this.loadData();
}

/**
 * This function loads a map centered at the given latitude, longitude and zoom
 * parameters.
 * @param latitude The latitude for the center of the map.
 * @param longitude The longitude for the center of the map.
 * @param zoom The level of zoom.
 */
Simulator.prototype.createMap = function (latitude, longitude, zoom) {

    this.map = L.map('simulation-map').setView([latitude, longitude], zoom);
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">' +
    'OpenStreetMap</a> contributors'
    }).addTo(this.map);

};

Simulator.prototype.loadData = function() {
    console.log('>>> [simulator] Loading data...');
    this.groundstations = this.jrpc.get_gs_list(this.__listGSCb());
};

Simulator.prototype.__listGSCb =  function(results) {
    console.log('>>> [simulator] List of gs retrieved: ' + results);
};

var __DEFAULT_LATITUDE = 0;
var __DEFAULT_LONGITUDE = 0;
var __DEFAULT_ZOOM = 5;
var __simulator = new Simulator();

/**
 * Callback that loads the map when the IP address could be GeoLocated.
 * @param response The JSON-P response with the GeoLocation of the IP address.
 * @private
 */
function __location_cb(response){
    var ll = Location2LatLongArray(response['loc']);
    __simulator.createMap(ll[0], ll[1], __DEFAULT_ZOOM);
}

/**
 * Callback that loads the map when the IP address could not be GeoLocated.
 * @private
 */
function __location_failed_cb(){
    __simulator = new Simulator();
    __simulator
        .createMap(__DEFAULT_LATITUDE, __DEFAULT_LONGITUDE, __DEFAULT_ZOOM);
}

/**
 * Factory method that creates a new simulator object.
 */
function loadSimulator(){
    console.log('>>> [simulator] Configuring...');
    getLocation(__location_cb, __location_failed_cb);
}