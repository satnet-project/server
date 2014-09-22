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

    // Array with the users selected for batch operation
    var user_list = []; //new Array();
    var __USERNAME_DEFAULT_CLASS__ = "rr-e";
    var __DEBUG__ = true;

    // Event binding to handlers
    $(document).ready(function(){
    
        $(".userCheck")
            .on("click", __userCheck);

        $( "#verify" )
            .on("click", __verifyUser);
        $( "#block" )
            .on("click", __blockUser);
        $( "#unblock" )
            .on("click", __unblockUser);
        $( "#delete" )
            .on("click", __deleteUser);
        $( "#activate" )
            .on("click", __activateUser);
        $( "#deactivate" )
            .on("click", __deactivateUser);

        $( ".undo" )
            .on("click", __undoOperation);

    });
  
    /*
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> EVENT HANDLERS
    */
    
    // Event Handler, user selected:
    
    function __userCheck()
    {
        var array = $(this).prop("id").split("_");
        var user_id = array[1];
        if ( $(this).prop("checked") )
            { user_selected(user_id); }
        else
            { user_deselected(user_id); }
    }

    function __verifyUser()
    {
    
        if ( __DEBUG__ ) console.log("__verifyUser");
        if ( user_list.length == 0 )
            { show_error("No users selected."); return; }
        
        clear_user_details();
        do_verify(user_list);
        
    }

    function __blockUser()
    {
    
        if ( __DEBUG__ ) console.log("__blockUser");
        if ( user_list.length == 0 )
            { show_error("No users selected."); return; }

        clear_user_details();
        do_block(user_list);
        
    }
    
    function __unblockUser()
    {
    
        if ( __DEBUG__ ) console.log("__unblockUser");
        if ( user_list.length == 0 )
            { show_error("No users selected."); return; }

        clear_user_details();
        do_unblock(user_list);
        
    }
    
    function __deleteUser()
    {
    
        if ( __DEBUG__ ) console.log("__deleteUser");
        if ( user_list.length == 0 )
            { show_error("No users selected."); return; }
        
        clear_user_details();
        do_delete(user_list);
        
    }
    
    function __activateUser()
    {
    
        if ( __DEBUG__ ) console.log("__activateUser");
        if ( user_list.length == 0 )
            { show_error("No users selected."); return; }
        
        clear_user_details();
        do_activate(user_list);
        
    }
    
    function __deactivateUser()
    {
    
        if ( __DEBUG__ ) console.log("__deactivateUser");
        if ( user_list.length == 0 )
            { show_error("No users selected."); return; }
        
        clear_user_details();
        do_deactivate(user_list);
        
    }
    
    function __undoOperation()
    {
    
        if ( __DEBUG__ ) console.log("__undoOperation");
        
        var array = $(this).prop("id").split("_");
        var user_id = array[1];
        
        undo_operation(user_id);
        
    }
    
    // Additional functions
    
    function user_selected(user_id)
    {

        user_list.push(user_id);
        
        var data = { user_id: user_id };
        $.getJSON('/accounts/ajax/user_details/', data)
            .done( user_details_cb )
            .fail( console.log('user_details GET failed!') );
            
        $( "#details" ).show();
         
    }

    function user_deselected(user_id)
    {
    
        user_list.splice( $.inArray(user_id, user_list), 1);
        clear_user_details();
        
    }

    function clear_user_details()
    {
        
        $( "#details" ).hide();
        $( "#details-username" ).html("");
        $( "#details-email" ).html("");
        $( "#details-name" ).html("");
        $( "#details-organization" ).html("");
        $( "#details-country" ).html("");
        
    }


    function do_verify(user_list)
        { do_operation("verify", "green-action", user_list); }
    function do_block(user_list)
        { do_operation("block", "action", user_list); }
    function do_unblock(user_list)
        { do_operation("unblock", "green-action", user_list); }
    function do_delete(user_list)
        { do_operation("delete", "red-action", user_list); }
    function do_activate(user_list)
        { do_operation("activate", "green-action", user_list); }
    function do_deactivate(user_list)
        { do_operation("deactivate", "action", user_list); }
        
    function do_operation(operation, css_class, user_list)
    {
    
        for ( var i = 0; i < user_list.length; i++ )
        {
        
            var u = user_list.pop();    // user identifier
            var n = "n_" + u;           // username selector
            var c = "c_" + u;           // checkbox selector
            var b = "u_" + u;           // undo button selector
            var h = "h_" + u;           // hidden field
            
            if ( __DEBUG__ )
                console.log(">>> op = " + operation + ", id = " + u +
                                ", n = " + n + ", c = " + c + ", b = " + b );
            
            // set operation
            $( "#" + h ).attr("value", operation);
            
            // change CSS decoration
            $( "#" + n ).removeClass(__USERNAME_DEFAULT_CLASS__)
                        .addClass(css_class);
            
            // hide checkbox and show undo button
            $( "#" + c ).hide().prop("checked", false);
            $( "#" + b ).show();
            
        }
    
        if ( __DEBUG__ )
            console.log("### user_list = " + user_list );
    
    }
    
    function undo_operation(user)
    {
    
        var n = "n_" + user;       // username selector
        var c = "c_" + user;       // checkbox selector
        var b = "u_" + user;       // undo button selector
            
        if ( __DEBUG__ )
                console.log(">>> undo, id = " + user +
                                ", n = " + n + ", c = " + c + ", b = " + b );
            
        // set operation and change CSS class
        $( "#" + n ).attr("op", "").attr("class", "")
            .addClass(__USERNAME_DEFAULT_CLASS__);

        // show checkbox and hide undo button
        $( "#" + c ).show();
        $( "#" + b ).hide();
    
    }

    function show_error(msg)
    {
    
        if ( __DEBUG__ ) console.log(msg);
        
    }

    /* AJAX premise's callback functions */

    function user_details_cb(response)
    {
        
        $( "#details-username" ).html(response.username);
        $( "#details-email" ).html(response.email);
        $( "#details-name" )
            .html(response.last_name + ", " + response.first_name);
        $( "#details-organization" ).html(response.organization);
        $( "#details-country" ).html(response.country);

    }

