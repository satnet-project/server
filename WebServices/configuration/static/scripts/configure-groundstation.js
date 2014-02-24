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
var __DEBUG__ = true;
// JRPC Client.
var __jrpc = null;

// Event binding to handlers
$(document).ready(function() {
    adapt_gs_dialog();
    $( "#gs_dialog_submit" ).on("click", submit_gs_dialog);
    $( "#gs_dialog_cancel" ).on("click", hide_gs_dialog);
    __jrpc = new ConfigurationService_JRPC();
});

function adapt_gs_dialog() {
    $('#edit-gs-button').puibutton({ icon: 'ui-icon-scissors', text: 'Edit',
        click: function() {
            var gs_id = $(this).attr('data-gs-id');
            console.log('Edit ground station, gs_id = ' + gs_id);
            __jrpc.getGroundStationConfiguration(__cb_load_gs_dialog, gs_id);
        }
    });
    $('#delete-gs-button').puibutton({ icon: 'ui-icon-close', text: 'Delete',
        click: function() {
            var gs_id = $(this).attr('data-gs-id');
            console.log('Delete ground station, gs_id = ' + gs_id);
            if ( confirm('Are you sure you want to delete this GS?') == false )
                { return; }
            __jrpc.deleteGroundStation(__cb_delete_gs, gs_id);
        }
    });
}

function clean_gs_dialog() {
    document.getElementById('id_gs_id').value = '';
    document.getElementById('id_gs_callsign').value = '';
    document.getElementById('id_gs_elevation').value = '';
}

function fill_gs_dialog(result) {
    document.getElementById('id_gs_id').value
        = document.getElementById('edit-gs-button').getAttribute('data-gs-id');
    document.getElementById('id_gs_callsign').value
        = result[__jrpc.GS_CALLSIGN];
    document.getElementById('id_gs_elevation').value
        = result[__jrpc.GS_ELEVATION];
    document.getElementById('id_latitude').value
        = result[__jrpc.GS_LATLON][0];
    document.getElementById('id_longitude').value
        = result[__jrpc.GS_LATLON][1];
}

function show_gs_dialog() {
    $( "#gs_dialog" ).show();
    $( "#gs_dialog_overlay" ).show();
    __load_map();
}

function hide_gs_dialog() {
    $( "#gs_dialog" ).hide();
    $( "#gs_dialog_overlay" ).hide();
    clean_gs_dialog();
}

function submit_gs_dialog() {
    var gs_id
        = document.getElementById('edit-gs-button').getAttribute('data-gs-id');
    if ( document.getElementById('id_gs_callsign').checkValidity() == false ) {
        alert('Wrong CALLSING identifier, must meet: [a-zA-Z0-9]{1,6}');
        return;
    }
    var cfg = create_gs_cfg();
    if (__DEBUG__) { console.log('cfg>>>>'); console.log(cfg); }
    __jrpc.setGroundStationConfiguration(__cb_set_gs_cfg, gs_id, cfg);
    hide_gs_dialog();
}

function create_gs_cfg() {
    var cfg = {};
    cfg[__jrpc.GS_CALLSIGN]
        = document.getElementById('id_gs_callsign').value;
    cfg[__jrpc.GS_ELEVATION]
        = document.getElementById('id_gs_elevation').value;
    var lat = document.getElementById('id_latitude').value;
    var lon = document.getElementById('id_longitude').value;
    cfg[__jrpc.GS_LATLON] = [lat, lon];
    return cfg;
}

/**
 * ////////////////////////////////////////////////////////////////////////////
 * ///////////////////////////////////////////////////////////////// Callbacks
 * ////////////////////////////////////////////////////////////////////////////
 */

function __cb_load_gs_dialog(result) {
    __log_cb('__cb_load_gs_dialog', result);
    fill_gs_dialog(result);
    show_gs_dialog();
}

function __cb_delete_gs(result) {
    __log_cb('__cb_delete_gs', result);
    if ( result ) { alert('Ground Station successfully deleted!'); }
    window.location.assign('/configuration/list_groundstations/');
}

function __cb_set_gs_cfg(result) {
    __log_cb('__cb_delete_gs', result);
    if ( result ) { alert('Ground Station successfully updated!'); }
    hide_gs_dialog();
    window.location.reload(true);
}
