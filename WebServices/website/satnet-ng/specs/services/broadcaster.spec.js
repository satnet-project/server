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

describe("Unit: Testing Services", function () {

    'use strict';

    describe("Broadcaster Services:", function () {

        beforeEach(module('broadcaster'));

        it('should contain a broadcaster',
            inject(function (broadcaster) {
                expect(broadcaster).not.toBeNull();
            }));

        it('should contain event keys',
            inject(function (broadcaster) {
                expect(broadcaster.GS_ADDED_EVENT).toBe('gs.added');
                expect(broadcaster.GS_REMOVED_EVENT).toBe('gs.removed');
                expect(broadcaster.GS_UPDATED_EVENT).toBe('gs.updated');
                expect(broadcaster.SC_ADDED_EVENT).toBe('sc.added');
                expect(broadcaster.SC_REMOVED_EVENT).toBe('sc.removed');
                expect(broadcaster.SC_UPDATED_EVENT).toBe('sc.updated');
            }));

    });

});