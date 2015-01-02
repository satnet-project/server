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

describe('Test Broadcaster Service', function () {
    'use strict';

    var rootScope, broadcaster, __id__ = 'test-gs';

    beforeEach(function () {
        module('broadcaster');
    });
    beforeEach(inject(function (_broadcaster_) {
        broadcaster = _broadcaster_;
    }));
    beforeEach(inject(function ($injector) {
        rootScope = $injector.get('$rootScope');
        spyOn(rootScope, '$broadcast');
    }));

    it('should return a broadcaster object', function () {
        expect(broadcaster).not.toBeNull();
    });

    it('should implement the expected API', function () {
        expect(broadcaster.GS_ADDED_EVENT).toBe('gs.added');
        expect(broadcaster.GS_REMOVED_EVENT).toBe('gs.removed');
        expect(broadcaster.GS_UPDATED_EVENT).toBe('gs.updated');
        expect(broadcaster.SC_ADDED_EVENT).toBe('sc.added');
        expect(broadcaster.SC_REMOVED_EVENT).toBe('sc.removed');
        expect(broadcaster.SC_UPDATED_EVENT).toBe('sc.updated');
    });

    it('should broadcast those events properly', function () {
        broadcaster.gsAdded(__id__);
        expect(rootScope.$broadcast).toHaveBeenCalledWith('gs.added', __id__);
        broadcaster.gsUpdated(__id__);
        expect(rootScope.$broadcast).toHaveBeenCalledWith('gs.updated', __id__);
        broadcaster.gsRemoved(__id__);
        expect(rootScope.$broadcast).toHaveBeenCalledWith('gs.removed', __id__);
        broadcaster.scAdded(__id__);
        expect(rootScope.$broadcast).toHaveBeenCalledWith('sc.added', __id__);
        broadcaster.scUpdated(__id__);
        expect(rootScope.$broadcast).toHaveBeenCalledWith('sc.updated', __id__);
        broadcaster.scRemoved(__id__);
        expect(rootScope.$broadcast).toHaveBeenCalledWith('sc.removed', __id__);
    });

});