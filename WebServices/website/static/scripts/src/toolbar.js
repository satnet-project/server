/*
   Copyright 2013, 2014 Ricardo Tubio-Pardavila

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

var toolbar = new Toolbar('toolbar');

/**
 * Toolbar class constructor.
 * @constructor
 * @param toolbar_div_id Id of the div that contains the toolbar.
 */
function Toolbar(toolbar_div_id) {
    this._DIV_ID = toolbar_div_id;
    this._SLIDE_EFFECT = 'slide';
    this._SLIDE_DURATION = 500;
    this._HIDE_DIRECTION = 'left';
    this._SHOW_DIRECTION = 'right';
}

/**
 * This method hides the toolbar using a slide-to-the-left animation effect.
 */
Toolbar.prototype.hide = function() {
    console.log('Hiding div with id = ', this._DIV_ID);
    $( '#' + this._DIV_ID ).toggle();
//        this._SLIDE_EFFECT,
//        { direction: this._HIDE_DIRECTION },
//        this._SLIDE_DURATION
//    );
};

/**
 * This method shows the toolba rusing a slide-to-the-right animation effect.
 */
Toolbar.prototype.show = function() {
    console.log('Showing div with id = ', this._DIV_ID);
    $( '#' + this._DIV_ID ).toggle( 'slow' );
//        this._SLIDE_EFFECT,
//        { direction: this._SHOW_DIRECTION },
//        this._SLIDE_DURATION
//    );
};
