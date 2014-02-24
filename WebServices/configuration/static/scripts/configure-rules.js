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
    adapt_rules_dialog();
    $( "#rules_dialog_submit" ).on("click", submit_rules_dialog);
    $( "#rules_dialog_cancel" ).on("click", hide_rules_dialog);
    __jrpc = new ConfigurationService_JRPC();
});

function adapt_rules_dialog() {
    $('.rule-ch').puibutton({ icon: 'ui-icon-newwin', text: 'Add Rule',
        click: function() {
            var gs_id = $(this).attr('data-gs-id');
            var ch_id = $(this).attr('data-ch-id');
            console.log('Add new availability rule, gs_id = ' + gs_id
                            + ', ch_id = ' + ch_id);
            show_rules_dialog(gs_id, ch_id);}});
    $('.input_date').datepicker({minDate: new Date()}).prop('disabled', false);
    $('.input_time').timepicker
        ({ step: 15, forceRoundTime: true, timeFormat: __TIME_FORMAT })
        .prop('disabled', false);
    $('.input_w_time').timepicker
        ({ step: 15, forceRoundTime: true, timeFormat: __TIME_FORMAT })
        .prop('disabled', true);
}

function rules_period_change(select) {
    var p = select.getElementsByTagName("option")[select.selectedIndex];
    if (__DEBUG__) { console.log('rules_period_change(), e = ' + select.id
                                    + ', p = ' + p.value); }
    if ( p.value == 'once_rule' ) { show_once(); }
    if ( p.value == 'daily_rule' ) { show_daily(); }
    if ( p.value == 'weekly_rule' ) { show_weekly(); }
}

function activate_input_time(input) {
    var day = input.getAttribute('data-day');
    if ( input.checked )
    {
        document.getElementById('id_rules_i_time_' + day).disabled = false;
        document.getElementById('id_rules_f_time_' + day).disabled = false;
    }
    else
    {
        document.getElementById('id_rules_i_time_' + day).disabled = true;
        document.getElementById('id_rules_f_time_' + day).disabled = true;
    }
}

function show_rules_dialog(gs_id, ch_id) {
    clean_rules_dialog();
    __jrpc.getGroundStationChannels(__cb_gs_channels, gs_id);
    show_once();
    $( "#rules_dialog" ).show();
    $( "#rules_dialog_overlay" ).show();
}

function show_once() {
    if (__DEBUG__) { console.log('show_once()'); }
    select_options('id_rules_period', 'once_rule');
    $("#div_i_date").show();
    $("#div_f_date").hide();
    $("#div_i_time").show();
    $("#div_f_time").show();
    $('#div_week').hide();
}

function show_daily() {
    if (__DEBUG__) { console.log('show_daily()'); }
    select_options('id_rules_period', 'daily_rule');
    $("#div_i_date").show();
    $("#div_f_date").show();
    $("#div_i_time").show();
    $("#div_f_time").show();
    $('#div_week').hide();
}

function show_weekly() {
    if (__DEBUG__) { console.log('show_weekly()'); }
    select_options('id_rules_period', 'weekly_rule');
    $("#div_i_date").show();
    $("#div_f_date").show();
    $("#div_i_time").hide();
    $("#div_f_time").hide();
    $('#div_week').show();
}

function hide_rules_dialog() {
    clean_rules_dialog();
    $( "#rules_dialog" ).hide();
    $( "#rules_dialog_overlay" ).hide();
}

function clean_rules_dialog() {
    remove_select_options('id_rules_chs');
    select_option_per_value('id_rules_period', 'once_rule');
    $('.input_time').timepicker('setTime');
    $('.input_w_check').prop('checked', false);
    $('.input_w_time').timepicker('setTime').prop('disabled', true);
}

function submit_rules_dialog() {
    var rule_cfg = validate_rules_dialog();
    if ( __DEBUG__ ) console.log('>>> rule_cfg read:');
    if (__DEBUG__) console.log(rule_cfg);
    var gs_id = document.getElementById('create-ch-rule')
                            .getAttribute('data-gs-id');
    var chs = get_selected_options('id_rules_chs');
    if (__DEBUG__) console.log('gs_id = ' + gs_id);
    for ( var i = 0; i < chs.length; i++ ) {
        if ( __DEBUG__ ) console.log('Adding rule to ch_id = ' + chs[i]);
        __jrpc.addAvailabilityRule
                (__cb_create_rule, gs_id, chs[i], rule_cfg);
    }
}

/**
 * ////////////////////////////////////////////////////////////////////////////
 * //////////////////////////////////////////////////////// Process Dialog Data
 * ////////////////////////////////////////////////////////////////////////////
 */

function validate_rules_dialog() {
    var chs = get_selected_options('id_rules_chs');
    if ( ( chs == null ) || ( chs.length == 0 ) )
        { __log_error('No channels selected.'); }
    if ( __DEBUG__ ) console.log('chs = ' + chs);
    return validate_rule_cfg();
}

function validate_rule_cfg() {
    var op = get_rule_operation();
    var period = get_rule_period();
    var dates = get_dates(period);
    var rule_cfg = {};
    rule_cfg[__jrpc.RULE_OP] = op;
    rule_cfg[__jrpc.RULE_PERIODICITY] = period;
    rule_cfg[__jrpc.RULE_DATES] = dates;
    return rule_cfg;
}

function get_rule_operation() {
    var op = get_selected_option('id_rules_ops');
    if ( op == 'add_rule' ) { return __jrpc.RULE_OP_ADD; }
    if ( op == 'delete_rule' ) { return __jrpc.RULE_OP_REMOVE; }
    throw 'Defined operation not supported.';
}

function get_rule_period() {
    var period = get_selected_option('id_rules_period');
    if ( period == 'once_rule' )
        { return __jrpc.RULE_PERIODICITY_ONCE; }
    if ( period == 'daily_rule' )
        { return __jrpc.RULE_PERIODICITY_DAILY; }
    if ( period == 'weekly_rule' )
        { return __jrpc.RULE_PERIODICITY_WEEKLY; }
    throw 'Defined period not supported.';
}

function get_dates(period) {
    if ( period == __jrpc.RULE_PERIODICITY_ONCE )
        { return get_once_dates(); }
    if ( period == __jrpc.RULE_PERIODICITY_DAILY )
        { return get_daily_dates(); }
    if ( period == __jrpc.RULE_PERIODICITY_WEEKLY )
        { return get_weekly_dates(); }
    throw 'Period not supported.';
}

function get_once_dates() {
    var date = read_date('id_rules_i_date');
    var starting_time = read_time_only('id_rules_i_time');
    var ending_time = read_time_only('id_rules_f_time');
    // For comparison...
    var initial_date = read_date_time('id_rules_i_date', 'id_rules_i_time');
    var final_date = read_date_time('id_rules_i_date', 'id_rules_f_time');
    if ( initial_date.getTime() >= final_date.getTime() )
        { __log_error('Initial date has to be smaller than final date.'); }
    var dates = {};
    dates[__jrpc.RULE_ONCE_DATE] = date.toJSON();
    dates[__jrpc.RULE_ONCE_S_TIME] = starting_time;
    dates[__jrpc.RULE_ONCE_E_TIME] = ending_time;
    return dates;
}

function get_daily_dates() {
    var initial_date = read_date('id_rules_i_date');
    var final_date = read_date('id_rules_f_date');
    if ( initial_date.getTime() >= final_date.getTime() )
        { __log_error('Initial date has to be smaller than final date.'); }
    var dates = {};
    var start_time = read_time_only('id_rules_i_time');
    var end_time = read_time_only('id_rules_i_time');
    dates[__jrpc.RULE_DAILY_I_DATE] = initial_date.toJSON();
    dates[__jrpc.RULE_DAILY_F_DATE] = final_date.toJSON();
    dates[__jrpc.RULE_S_TIME] = start_time;
    dates[__jrpc.RULE_E_TIME] = end_time;
    return dates;
}

function get_weekly_dates() {
    var initial_date = read_date('id_rules_i_date');
    var final_date = read_date('id_rules_f_date');
    if ( initial_date.getTime() >= final_date.getTime() )
        { __log_error('Initial date has to be smaller than final date.'); }
    var dates = {};
    dates[__jrpc.RULE_WEEKLY_DATE] = [];
    for ( var i = 0; i < __jrpc.RULE_WEEKDAYS.length; i++ ) {
        var d = __jrpc.RULE_WEEKDAYS[i];
        if ( document.getElementById('id_rules_check_' + d).checked == false )
            { continue; }
        var i_time = read_time_only('id_rules_i_time_' + d),
            f_time = read_time_only('id_rules_f_time_' + d);
        if ( compare_str_time(i_time, f_time) == false ) {
            __log_error('Initial time must be smaller than final, day = ' + d);
        }
        var date = {};
        date[__jrpc.RULE_WEEKLY_DATE_DAY] = d;
        date[__jrpc.RULE_S_TIME] = i_time;
        date[__jrpc.RULE_E_TIME] = f_time;
        dates[__jrpc.RULE_WEEKLY_DATE].push(date);
    }
    return dates;
}

/**
 * ////////////////////////////////////////////////////////////////////////////
 * ///////////////////////////////////////////////////////////////// Callbacks
 * ////////////////////////////////////////////////////////////////////////////
 */

function __cb_gs_channels(result) {
    __log_cb('__cb_gs_channels', result);
    var channels = result[__jrpc.GS_CHANNELS];
    fill_select_options('id_rules_chs', channels);
}

function __cb_create_rule(result) {
    __log_cb('__cb_create_rule', result);
    hide_rules_dialog();
}
