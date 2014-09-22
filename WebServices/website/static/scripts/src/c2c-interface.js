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
 * New GroundStation button clicked.
 * @private
 */
function __add_gs_event() {
    console.log('>>>  Add GS clicked!')
}

/**
 * New Spacecraft button clicked.
 * @private
 */
function __add_sc_event() {
    console.log('>>>  Add SC clicked!')
}

/**
 * This function connects all the events from the DOM with its handlers.
 * @private
 */
function __loadEventHandlers() {
    document.getElementById("button_add_gs").onclick = __add_gs_event;
    document.getElementById("button_add_sc").onclick = __add_sc_event;
}

/**
 * Main function that connects the DOM tree with the event handlers.
 */
function loadC2CInterface() {
    console.log('>>> Loading C2C Interface...');
    __loadEventHandlers();
}
