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

describe('Test X-Satnet Service', function () {
    'use strict';

    var xSatnetRPC, jsonrpcMock;

    beforeEach(module('x-satnet-services', function ($provide) {
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

    beforeEach(inject(function (_xSatnetRPC_) {
        xSatnetRPC = _xSatnetRPC_;
    }));

    it('should return a satnetRPC object', function () {
        console.log('>>> xSatnetRPC = ' + JSON.stringify(xSatnetRPC));
        expect(xSatnetRPC).not.toBeNull();
    });

});