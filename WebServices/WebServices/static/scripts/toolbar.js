/* Copyright 2013, 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License. */

    // This variable holds the id of the last marked button
    var marked_id = '';
    var __DEBUG__ = true;
    var __MARK_ACTIVATED_CLASS__ = 'activated-mark';
    var __MARK_DEACTIVATED_CLASS__ = 'deactivated-mark';
    
    $(document).ready(function(){
    
        $(".button-entry")
            .on("click", __menuButton);
            
    });
    
    function __menuButton()
    {
    
        if ( __DEBUG__ )
            console.log('>> Detecetd click on a <button-entry> class.');

        var array = $(this).prop("id").split("_");
        var label = array[1];
        var mark_id = 'mark_' + label;
        
        if ( __DEBUG__ )
            console.log('>> mark = ' + mark_id);
        
        if ( mark_id == marked_id )
            { return; }
            
        if ( __DEBUG__ )
            console.log('>> still unmarked, go ahead!');

        if ( marked_id != '' )
            { deactivateMark(marked_id); }

        activateMark(mark_id);
        
    }
        
    function activateMark(mark_id)
    {
        $( "#" + mark_id ).attr("class", "")
            .addClass(__MARK_ACTIVATED_CLASS__);
        marked_id = mark_id;          
    }
    
    function deactivateMark(mark_id)
    {
        $( "#" + mark_id ).attr("class", "")
            .addClass(__MARK_DEACTIVATED_CLASS__);
    }

