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

describe('Test Maps Service', function () {
    'use strict';

    var maps, satnetRPCMock, leafletDataMock;

    beforeEach(module('map-services', function ($provide) {
        satnetRPCMock = {};
        satnetRPCMock.rCall = jasmine.createSpy();
        leafletDataMock = {};
        $provide.value('satnetRPC', satnetRPCMock);
        $provide.value('leafletData', leafletDataMock);
    }));

    beforeEach(inject(function (_maps_) {
        maps = _maps_;
    }));

    it('should return a maps object', function () {
        expect(maps).not.toBeNull();
        console.log('>>> maps = ' + JSON.stringify(maps));
    });

    it('should declare constants: LAT, LNG, ZOOM and T_OPACITY', function () {
        expect(maps.T_OPACITY).toBe(0.125);
        expect(maps.LAT).toBe(37.7833);
        expect(maps.LNG).toBe(-122.4167);
        expect(maps.ZOOM).toBe(7);
    });

    /*
    it('should center a map according to angular-leaflet', function () {
        var __scope__ = {},
            __lat__ = 37.7833,
            __lng__ = -122.4167,
            __zoom__ = 7;
        maps.centerMap(__scope__, __lat__, __lng__, __zoom__);
        expect(__scope__).toBe({
            center: {
                lat: __lat__,
                lng: __lng__,
                zoom: __zoom__
            },
            markers: {
                gs: {
                    lat: __lat__,
                    lng: __lng__,
                    focus: true,
                    draggable: true,
                    label: {
                        message: 'Drag me!',
                        options: {
                            noHide: true
                        }
                    }
                }
            },
            baselayers: {
                osm_baselayer: {
                    name: 'OSM Base Layer',
                    type: 'xyz',
                    url: 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                    layerOptions: {
                        noWrap: true,
                        continuousWorld: false,
                        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                    }
                }
            }
        });
    });
    */
});