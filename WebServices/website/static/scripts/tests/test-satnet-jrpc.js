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

module('satnet-jrpc-test');

QUnit.test("get-groundstations-list", function(assert) {

    console.log('testxxxx');
    assert.expect(1);
    console.log('2');

    new $.JsonRpcClient({ ajaxUrl: 'http://127.0.0.1:8000/jrpc' }).call(
        'configuration.gs.list', [ ],
        function(result) {
            //alert('Foo bar answered: ' + result.my_answer);
            console.log('callback, result = ', result);
            assert.ok(1, true, 'ok');
            QUnit.start();
        },
        function(error) {
            console.log('There was an error = '); console.log(error);
            assert.ok(1, false, 'nok');
            QUnit.start();
        }
    );

    assert.ok(1, true, 'ok');

});
