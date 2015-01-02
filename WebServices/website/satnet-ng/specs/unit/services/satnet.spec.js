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

describe('Test Satnet Service', function () {
    'use strict';

    var satnetRPC, jsonrpcMock, $httpBackend, rootScope,
        getUserLocation = '/configuration/user/geoip',
        getServerLocation = '/configuration/hostname/geoip',
        __LAT__ = 35.347099, __LNG__ = -120.455299;

    beforeEach(module('satnet-services', function ($provide) {
        jsonrpcMock = {};
        jsonrpcMock.results = {};
        jsonrpcMock.newService = function (name, rpc) {
            return {
                jsonrpc_mock: this,
                service: name,
                rpc: rpc,
                createMethod: function (name) {
                    return function (params) {
                        jsonrpcMock.results[name] = '@createMethod, name = ' +
                            name + ', params = ' + JSON.stringify(params);
                        return jsonrpcMock.results[name];
                    };
                }
            };
        };
        $provide.value('jsonrpc', jsonrpcMock);
    }));

    beforeEach(inject(function (_satnetRPC_, _$httpBackend_, _$rootScope_) {
        satnetRPC = _satnetRPC_;
        $httpBackend = _$httpBackend_;
        rootScope = _$rootScope_;
        $httpBackend.when('GET', getUserLocation).respond(
            {latitude: __LAT__, longitude: __LNG__}
        );
        $httpBackend.when('POST', getServerLocation).respond(
            {latitude: __LAT__, longitude: __LNG__}
        );
    }));

    afterEach(function () {
        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
    });

    it('should return a satnetRPC object', function () {
        expect(satnetRPC).not.toBeNull();
    });

    it('should throw an exception if the method does not exist', function () {
        var __non_existing_method__ = 'x';
        expect(function () { satnetRPC.rCall(__non_existing_method__, []); })
            .toThrow(
                '[satnetRPC] service not found, id = <' +
                    __non_existing_method__ + '>'
            );
    });

    it('should provide an estimated location of the user', function () {
        $httpBackend.expectGET(getUserLocation);
        rootScope.user_geoip = {};
        satnetRPC.getUserLocation().then(function (data) {
            angular.extend(rootScope.user_geoip, data);
        });
        $httpBackend.flush();
        expect(rootScope.user_geoip.latitude).toBe(__LAT__);
        expect(rootScope.user_geoip.longitude).toBe(__LNG__);
    });

    it('should provide an estimated location of a host', function () {
        var __hostname__ = 'localhost';
        $httpBackend.expectPOST(getServerLocation);
        rootScope.hostname_geoip = {};
        satnetRPC.getServerLocation(__hostname__).then(function (data) {
            angular.extend(rootScope.hostname_geoip, data);
        });
        $httpBackend.flush();
        expect(rootScope.hostname_geoip.latitude).toBe(__LAT__);
        expect(rootScope.hostname_geoip.longitude).toBe(__LNG__);
    });

});