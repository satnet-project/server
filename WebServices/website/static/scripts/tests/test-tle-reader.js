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

////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////// ANGULAR DEPENDENCY INJECTION
////////////////////////////////////////////////////////////////////////////////

var app = angular.module('app', [ 'ngCookies' ])
    .run(function($http, $cookies){
        $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
    });
var injector = angular.injector(['ng', 'app']);
var init = {
    setup: function() {
        this.$scope = injector.get('$rootScope').$new();
    }
};

////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////// ACTUAL TEST
////////////////////////////////////////////////////////////////////////////////

module('tle-reader-test', init);

QUnit.asyncTest( "[tle-reader] Read single TLE file...", function( assert ) {

    expect(1);

    var tle_reader = new TLEReader(
        injector.get('$log'), injector.get('$http')
    );

    setTimeout(function() {
        assert.strictEqual(
            tle_reader.getSatellites().length, 99, 'Wrong raw data.'
        );
        QUnit.start();
    }, 1000);

});