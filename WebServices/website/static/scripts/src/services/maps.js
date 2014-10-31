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
 * Created by rtubio on 10/30/14.
 */

/** Module definition (empty array is vital!). */
angular.module('maps', []);

/**
 * Service used for broadcasting UI events in between controllers.
 */
angular.module('maps').service('maps', function () {
    
        'use strict';
        
        this.DEFAULT_LAT = 42.6000;    // lat, lon for Pobra (GZ/ES)
        this.DEFAULT_LNG = -8.9330;
        this.DEFAULT_ZOOM = 6;
        this.USER_ZOOM = 8;

        /**
         * This function centers the map at the given [lat, long] coordinates
         * with the specified zoom level.
         * @param map Leaflet map.
         * @param lat Latitude (coordinates).
         * @param lng Longitude (coordinates).
         * @param zoom Level of zoom.
         */
        this.centerMap = function (map, lat, lng, zoom) {
            map.setView(new L.LatLng(lat, lng), zoom);
        };

        /**
        * This function locates the map at the location of the IP that the
        * client uses for this connection.
        * @param $log AngularJS logger object.
        * @param map The map where the user position is to be located.
        * @param marker OPTIONAL parameter with a reference to a marker object that is
        *                  suppose to hold current user's position.
        */
        this.locateUser = function ($log, map, marker) {

            $.get('http://ipinfo.io', function (data) {
                var ll = data.loc.split(',');
                var lat = parseFloat(ll[0]);
                var lng = parseFloat(ll[1]);
                $log.info('[map-ctrl] User located at = ' + ll);
                this.centerMap(map, lat, lng, this.USER_ZOOM);
                if ( marker !== null ) { marker.lat = lat; marker.lng = lng; }
            }, 'jsonp')
            .fail( function() {
                $log.warn('[map-ctrl] Could not locate user');
                this.centerMap(
                    map,
                    this.DEFAULT_LAT, this.DEFAULT_LNG,
                    this.DEFAULT_ZOOM
                );
                if ( marker !== null ) {
                    marker.lat = this.DEFAULT_LAT;
                    marker.lng = this.DEFAULT_LNG;
                }
            });

        };

    }
);