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
 *
 * Created by rtubio on 1/31/14.
 */

__DEBUG__ = true;

function __log_error(msg)
    { if(__DEBUG__) console.log(msg); alert(msg); throw msg; }

function __log_cb(cb_name, result) {
    if (__DEBUG__) console.log(cb_name);
    if (__DEBUG__) console.log(result);
}

/*
/////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////// DATE & TIME
/////////////////////////////////////////////////////////////////////////////
 */

var __DATE_SEPARATOR = '-';
var __DATE_TIME_SEPARATOR = '-';
var __TIME_SEPARATOR = ':';
var __DATE_FORMAT = 'yyyy' + __DATE_SEPARATOR + 'mm' + __DATE_SEPARATOR + 'dd';
var __TIME_FORMAT = 'H' + __TIME_SEPARATOR + 'i';
var __0_DATE = '01/01/1970';

function get_year(date_str)
    { return(date_str.split(__DATE_SEPARATOR)[0]); }
function get_month(date_str)
    { return(date_str.split(__DATE_SEPARATOR)[1]); }
function get_day(date_str)
    { return(date_str.split(__DATE_SEPARATOR)[2]); }

function get_hour(time_str)
    { return(time_str.split(__TIME_SEPARATOR)[0]); }
function get_minutes(time_str)
    { return(time_str.split(__TIME_SEPARATOR)[1]); }

function compare_str_time(time_a, time_b) {
    if (__DEBUG__) { console.log('time_a = ' + time_a + ', parsed = '
                        + Date.parse(__0_DATE + ' ' + time_a)); }
    if (__DEBUG__) { console.log('time_b = ' + time_b + ', parsed = '
                        + Date.parse(__0_DATE + ' ' + time_b)); }
    return  Date.parse(__0_DATE + ' ' + time_a) <
            Date.parse(__0_DATE + ' ' + time_b);
}

function get_Hi_from_date(date)
    { return(date.getHours() + __TIME_SEPARATOR + date.getMinutes()); }

function read_date(datepicker_id) {
    var date = $( '#' + datepicker_id ).datepicker('getDate');
    if ( date == null ) { __log_error('Date not set.'); }
    return date;
}

function read_time_only(timepicker_id) {
    var time = $( '#' + timepicker_id ).val();
    if ( ( time == null ) || ( time.length == 0 ) )
        { __log_error('Time not set.'); }
    return time;
}

function read_time(timepicker_id, date) {
    if ( date == null ) { date = new Date(); }
    var time = $( '#' + timepicker_id ).val();
    if ( ( time == null ) || ( time.length == 0 ) )
        { __log_error('Time not set.'); }
    date.setHours(get_hour(time));
    date.setMinutes(get_minutes(time));
    return date;
}

function read_date_time(datepicker_id, timepicker_id) {
    var date = read_date(datepicker_id);
    return read_time(timepicker_id, date);
}

/*
/////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////// SELECT OPTIONS
/////////////////////////////////////////////////////////////////////////////
 */

function init_select_options(select_id) {
    var e = document.getElementById(select_id);
    var option = document.createElement("option");
    option.text = "(Loading... wait!)";
    e.add(option, null);
}

function fill_select_options(select_id, options) {
    var e = document.getElementById(select_id);
    $.each(options, function(k, v) {
        var option = document.createElement("option");
        option.text = v;
        option.value = v;
        e.add(option, null);
    });
}

function select_band(component_id, band) {
    var select = document.getElementById(component_id);
    for ( var i = 0, l = select.options.length, o; i < l; i++ ) {
        o = select.options[i];
        if (o.text == band) {o.selected = true; break;}
    }
}

function select_options(component_id, selections, toString) {
    var select = document.getElementById(component_id);
    var options = select.getElementsByTagName('option');
    for ( var i = 0, l = options.length, o; i < l; i++ ) {
        o = options[i];
        for ( var j = 0, s; j < selections.length; j++ ) {
            s = selections[j];
            if ( toString )
                { if ( s.toString(10) == o.text ) { o.selected = true; } }
            else
                { if ( s == o.text ) { o.selected = true; } }
        }
    }
}

function set_option_value(select_id, option_value) {
    var select = document.getElementById(select_id);
    var options = select.getElementsByTagName('option');
    for ( var i = 0; i < options.length; i++ ) {
        if ( options[i].value == option_value )
            { select.options[i].selected=true; break; }
    }
}

function select_option_per_value(select_id, option) {
    var options = document.getElementById(select_id)
                            .getElementsByTagName('option');
    for ( var i = 0, l = options.length, o; i < l; i++ ) {
        if ( options[i].value == option )
            { options[i].selected = true; break; }
    }
}

function remove_select_options(select_id) {
    var e = document.getElementById(select_id);
    for (var i = e.options.length; i > 0; i--)
        { e.options[i-1] = null; }
}

function clean_selected_options(select_id) {
    var e = document.getElementById(select_id);
    for (var i = 0; i < e.options.length; i++)
        { e.options[i].selected = false; }
}

function print_select_options(select_id) {
    var e = document.getElementById(select_id);
    console.log('>>> options for e.id = ' + select_id);
    for (var i = 0; i < e.options.length; i++)
        { console.log('o[' + i + ']' + e.options[i].text); }
}

function get_selected_option(select_id, option) {
    var s = document.getElementById(select_id);
    var v = s.getElementsByTagName("option")[s.selectedIndex].value;
    return(v);
}

function get_selected_options(select_id, option) {
    var r = [];
    var options = document.getElementById(select_id).options;
    for (var i = 0, s_len = options.length; i < s_len; i++) {
        var o  = options[i];
        if (o.selected) { r.push(o.value); }
    }
    return r;
}

/*
/////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////// TEXTAREA
/////////////////////////////////////////////////////////////////////////////
 */

var __REGEX_name = new RegExp('^[a-zA-Z0-9-\.]{6,9}$');

function init_textarea(textarea_id, text, disable) {
    var e = document.getElementById(textarea_id);
    e.value = text;
    e.className = 'textarea-initial';
    e.readOnly = disable;
}

function erase_textarea(textarea_id) {
    var e = document.getElementById(textarea_id);
    var name = e.value;
    if ( ( name != __NAME_initial_value) && ( name != '' ) ) { return; }
    e.value = '';
    e.className = '';
}

function validate_textarea(textarea_id, regex) {
    var e = document.getElementById(textarea_id);
    var text = e.value;
    var matches = new RegExp(regex).exec(text);
    if ( __DEBUG__ ) { console.log('Validating, REGEX = ' + regex
                                    + ', text = ' + text
                                    + ', matches = ' + matches); }
    if ( matches == null ) {
        e.style.color = 'red';
        e.style.fontWeight = 'bolder';
        return;
    }
    if ( matches.length == 1) {
        e.style.color = 'green';
        e.style.fontWeight = '';
    }
}

function supressEnterKey() { return ( event.keyCode || event.which ) != 13; }
