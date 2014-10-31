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
angular.module('common', []);

/**
 * Service used for broadcasting UI events in between controllers.
 */
angular.module('common').service('common', [ function () {

    'use strict';

    /**
     * This function locates the map at the location of the IP that the
     * client uses for this connection.
     */
     this.locateUser = function () {
         return $.get('http://ipinfo.io', function (data) {
             var ll = data.loc.split(',');
             var lat = parseFloat(ll[0]);
             var lng = parseFloat(ll[1]);
             return [ lat, lng ];
         }, 'jsonp');
    };

    // Proxy to get rid of the CORS restrictions.
    this._CORSS_PROXY = 'http://www.corsproxy.com/';
    // Get rid of this part of the URI to use with corsproxy
    this._CORSS_PROXY_HTTP = 'http://';

    /**
     * Returns a URL modified to be used directly with the corsproxy.com service.
     * @param url The URL to be modified.
     * @returns {string} The ready-to-use URL.
     */
    this.getCORSSURL = function (url) {
        var correctedUrl = url.replace(this._CORSS_PROXY_HTTP, '');
        return(this._CORSS_PROXY + correctedUrl);
    };
    
}]);