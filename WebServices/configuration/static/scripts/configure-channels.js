/**
 * Copyright 2014, 2014 Ricardo Tubio-Pardavila
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
 */

/**
 * Created by rtubio on 1/31/14.
 */

// Initial name for the input text areas
var __NAME_initial_value = 'Type a name';
// Array with the users selected for batch operation
var __DEBUG__ = true;

// Object that handles the invokation of the remote methods.
var __jrpc = null;

// Event binding to handlers
$(document).ready(function() {
    adapt_ch_dialog();
    $( "#add_channel_button" )
        .on("click", add_channel_dialog_load);
    $( "#channel_dialog_cancel_button" )
        .on("click", hide_channel_dialog);
    __jrpc = new ConfigurationService_JRPC();
});

function adapt_ch_dialog() {
    $('#add-ch-button').puibutton({ icon: 'ui-icon-newwin', text: '(+) channel',
        click: function() {
            var gs_id = $(this).attr('data-gs-id');
            add_channel_dialog_load();
        }
    });
    var edit_ch_buttons = document
           .getElementsByClassName('edit-ch');
    for(var i = 0; i < edit_ch_buttons.length; i++) {
        var e_b = edit_ch_buttons[i].id;
        add_edit_channel_components(e_b);
    }
    var delete_ch_buttons = document.getElementsByClassName('delete-ch');
    for(i = 0; i < delete_ch_buttons.length; i++) {
        e_b = delete_ch_buttons[i].id;
        add_delete_channel_components(e_b);
    }
}

function add_edit_channel_components(button_id) {
    $( "#" + button_id ).puibutton({ icon: 'ui-icon-scissors', text: 'Edit',
        click: function() {
            var ch_id = $(this).attr('data-ch-id');
            var gs_id = $(this).attr('data-gs-id');
            edit_channel_dialog_load(gs_id, ch_id);
        }
    });
}

function add_delete_channel_components(button_id) {
    $( "#" + button_id ).puibutton({ icon: 'ui-icon-close', text: 'Delete',
        click: function() {
            var channel_id = $(this).attr('data-ch-id');
            var gs_id = $(this).attr('data-gs-id');
            __jrpc.deleteChannel(__cb_delete_channel, gs_id, channel_id);
        }
    });
}

function add_channel_dialog_load() {
    $( "#channel_dialog_add_button" )
        .on("click", submit_add_channel_dialog);
    init_textarea('id_ch_name', __NAME_initial_value, false);
    init_select_options('id_ch_mod');
    init_select_options('id_ch_band');
    init_select_options('id_ch_bps');
    init_select_options('id_ch_bw');
    init_select_options('id_ch_pol');
    __jrpc.getChannelOptions(__cb_get_channel_options);
}

function edit_channel_dialog_load(gs_id, ch_id) {
    $( "#channel_dialog_add_button" )
        .on("click", submit_edit_channel_dialog);
    init_textarea('id_ch_name', ch_id, true);
    init_select_options('id_ch_mod');
    init_select_options('id_ch_band');
    init_select_options('id_ch_bps');
    init_select_options('id_ch_bw');
    init_select_options('id_ch_pol');
    __jrpc.getChannelOptions(__cb_select_channel_options);
}

function clean_channel_dialog() {
    $( "#id_ch_name" ).value = '';
    remove_select_options('id_ch_mod');
    remove_select_options('id_ch_band');
    remove_select_options('id_ch_bps');
    remove_select_options('id_ch_bw');
    remove_select_options('id_ch_pol');
}

function submit_edit_channel_dialog() {
    var cfg = create_channel_cfg();
    var gs_id = $( "#add-ch-button" ).attr('data-gs-id');
    var ch_id = document.getElementById('id_ch_name').value;
    __jrpc.setChannelConfiguration(__cb_set_channel_cfg, gs_id, ch_id, cfg);
}

function submit_add_channel_dialog() {
    var gs_id = $( "#add-ch-button" ).attr('data-gs-id');
    var ch_id = document.getElementById('id_ch_name').value;
    // correctness check
    if ( ch_id == __NAME_initial_value )
        { ch_id = ''; __log_error('No channel identifier provided!'); return; }
    if ( __REGEX_name.exec(ch_id) == null )
        { alert('Wrong channel name format.'); return; }
    __jrpc.verifyChannelId(__cb_verify_and_create, ch_id);
}

function show_channel_dialog() {
    $( "#add_channel_dialog" ).show();
    $( "#add_channel_dialog_overlay" ).show();
}

function hide_channel_dialog() {
    $( "#add_channel_dialog" ).hide();
    $( "#add_channel_dialog_overlay" ).hide();
    clean_channel_dialog();
}

function channel_dialog_show_options() {
    console.log('############### options BEGIN');
    print_select_options('id_ch_mod');
    print_select_options('id_ch_bw');
    print_select_options('id_ch_bps');
    print_select_options('id_ch_pol');
    console.log('############### options END');
}

function process_channel_options(result) {
    remove_select_options('id_ch_mod');
    fill_select_options('id_ch_mod', result[__jrpc.CH_MODS]);
    remove_select_options('id_ch_band');
    fill_select_options('id_ch_band', result[__jrpc.CH_BAND]);
    remove_select_options('id_ch_bps');
    fill_select_options('id_ch_bps', result[__jrpc.CH_BPS]);
    remove_select_options('id_ch_bw');
    fill_select_options('id_ch_bw', result[__jrpc.CH_BWS]);
    remove_select_options('id_ch_pol');
    fill_select_options('id_ch_pol', result[__jrpc.CH_POL]);
}

function select_channel_configuration(result) {
    init_channel_name('id_ch_name', result[__jrpc.CH_ID]);
    select_band('id_ch_band', result[__jrpc.CH_BAND]);
    select_options('id_ch_mod', result[__jrpc.CH_MODS], false);
    select_options('id_ch_bps', result[__jrpc.CH_BPS], true);
    select_options('id_ch_bw', result[__jrpc.CH_BWS], true);
    select_options('id_ch_pol', result[__jrpc.CH_POL], false);
}

function init_channel_name(textarea_id, name) {
    var e = document.getElementById(textarea_id);
    e.value = name;
    e.style.color = 'green';
    e.style.fontWeight = '';
    e.style.fontStyle = '';
}

function create_channel_cfg() {
    var cfg = { };
    cfg[__jrpc.CH_BAND] = get_selected_option('id_ch_band', "Band");
    cfg[__jrpc.CH_MODS] =
        get_selected_options('id_ch_mod', "Modulation");
    cfg[__jrpc.CH_BPS] =
        get_selected_options('id_ch_bps', "Bitrate");
    cfg[__jrpc.CH_POL] =
        get_selected_options('id_ch_pol', "Polarization");
    cfg[__jrpc.CH_BWS] =
        get_selected_options('id_ch_bw', "Bandwidth");
    return(cfg);
}

/**
 * ////////////////////////////////////////////////////////////////////////////
 * ///////////////////////////////////////////////////////////////// Callbacks
 * ////////////////////////////////////////////////////////////////////////////
 */

function __cb_verify_channel_id(result) {
    __log_cb('__cb_verify_channel_id', result);
    if ( result == true ) { alert('Channel ID already exists.'); }
}

function __cb_create_channel(result) {
    __log_cb('__cb_create_channel', result);
    if ( result == true ) { alert('Channel created succesfully!'); }
    hide_channel_dialog();
    window.location.reload(true);
}

function __cb_verify_and_create(result) {
    __log_cb('__cb_verify_channel_id', result);
    if ( result == true ) { alert('Channel ID already exists.'); return; }
    var channel_cfg = create_channel_cfg();
    var gs_id = $( "#add-ch-button" ).attr('data-gs-id');
    var ch_id = document.getElementById('id_ch_name').value;
    __jrpc.createChannel(__cb_create_channel, gs_id, ch_id, channel_cfg);
}

function __cb_delete_channel(result) {
    __log_cb('__cb_delete_channel', result);
    if ( result ) { alert('Channel deleted succesfully!'); }
    window.location.reload(true);
}

function __cb_get_channel_options(result) {
    __log_cb('__cb_get_channel_options', result);
    process_channel_options(result);
    show_channel_dialog();
}

function __cb_select_channel_options(result) {
    __log_cb('__cb_select_channel_cfg', result);
    process_channel_options(result);
    var gs_id = $( "#add-ch-button" ).attr('data-gs-id');
    var ch_id = document.getElementById('id_ch_name').value;
    __jrpc.getChannelConfiguration(__cb_select_channel_cfg, gs_id, ch_id)
}

function __cb_select_channel_cfg(result)
{
    __log_cb('__cb_select_channel_cfg', result);
    select_channel_configuration(result);
    show_channel_dialog();
}

function __cb_set_channel_cfg(result) {
    __log_cb('__cb_set_channel_cfg', result);
    if ( result ) { alert('Channel updated succesfully!'); }
    hide_channel_dialog();
    window.location.reload(true);
}
