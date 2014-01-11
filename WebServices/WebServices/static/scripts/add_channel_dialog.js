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

// Array with the users selected for batch operation
var __DEBUG__ = true;

// JRPC keys for accessing several data on the server
var __JRPC_key_gs_id = 'groundstation_id';
var __JRPC_key_name = 'name';
var __JRPC_key_band = 'band';
var __JRPC_key_modulations = 'modulations';
var __JRPC_key_bitrates = 'bitrates';
var __JRPC_key_bandwidths = 'bandwidths';
var __JRPC_key_polarizations = 'polarizations';

var __REGEX_name = new RegExp('^[a-zA-Z0-9-\.]{6,9}$');

var __NAME_initial_value = 'Type a name';

    // Event binding to handlers
    $(document).ready(function() {
        $( "#add_channel_button" )
            .on("click", add_channel_dialog_init);
        $( "#add_channel_dialog_add_button" )
            .on("click", add_channel_dialog_add);
        $( "#add_channel_dialog_cancel_button" )
            .on("click", add_channel_dialog_hide);
    });

    function add_channel_dialog_init()
    {
        init_textarea('id_ch_name');
        init_select_options('id_ch_mod');
        init_select_options('id_ch_band');
        init_select_options('id_ch_bps');
        init_select_options('id_ch_bw');
        init_select_options('id_ch_pol');

        __JRPC_get_options();

        $( "#add_channel_dialog" ).show();
        $( "#add_channel_dialog_overlay" ).show();
    }

    function add_channel_dialog_clean()
    {
        $( "#id_ch_name" ).value = '';
        clear_select_options('id_ch_mod');
        clear_select_options('id_ch_band');
        clear_select_options('id_ch_bps');
        clear_select_options('id_ch_bw');
        clear_select_options('id_ch_pol');
    }

    function add_channel_dialog_add()
    {
        var gs_id = $(this).prop('value');
        verify_channel_name('id_ch_name');
        try
        {
            var channel_cfg = create_channel_cfg(gs_id);
            if ( __DEBUG__ ) console.log(channel_cfg);

            var jrc = new $.JsonRpcClient({ ajaxUrl: '/jrpc/' });

            jrc.call(
                'configuration.gs.channel.create', [ channel_cfg ],
                function(result)
                {
                    console.log('Channel created succesfully!');
                    alert('Channel created succesfully!');
                    add_channel_dialog_hide();
                },
                function(error) { __error(error['message']); }
            );
        }
        catch(err) { __error(err); }
    }

    function add_channel_dialog_hide()
    {
        $( "#add_channel_dialog" ).hide();
        $( "#add_channel_dialog_overlay" ).hide();
        add_channel_dialog_clean();
    }

    function init_select_options(select_id)
    {
        var e = document.getElementById(select_id);
        var option = document.createElement("option");
        option.text = "(Loading... wait!)";
        e.add(option, null);
    }

    function fill_select_options(select_id, options)
    {
        var e = document.getElementById(select_id);
        $.each(options, function(k, v) {
            var option = document.createElement("option");
            option.text = v;
            option.value = v;
            e.add(option, null);
        });
    }

    function clear_select_options(select_id) {
        var e = document.getElementById(select_id);
        for (var i = 0; i < e.options.length; i++)
            { e.options[i] = null; }
    }

    function __JRPC_get_options() {

        var jrc = new $.JsonRpcClient({ ajaxUrl: '/jrpc/' });
        jrc.call(
            'configuration.gs.channel.getOptions', [],
            process_channel_options,
            function(error) { __error(error['message']); }
        );

    }

    function process_channel_options(result)
    {
        clear_select_options('id_ch_mod');
        fill_select_options('id_ch_mod', result[__JRPC_key_modulations]);
        clear_select_options('id_ch_band');
        fill_select_options('id_ch_band', result[__JRPC_key_band]);
        clear_select_options('id_ch_bps');
        fill_select_options('id_ch_bps', result[__JRPC_key_bitrates]);
        clear_select_options('id_ch_bw');
        fill_select_options('id_ch_bw', result[__JRPC_key_bandwidths]);
        clear_select_options('id_ch_pol');
        fill_select_options('id_ch_pol', result[__JRPC_key_polarizations]);
    }

    function create_channel_cfg(gs_id) {

        var cfg = { };

        cfg[__JRPC_key_gs_id] = gs_id;
        cfg[__JRPC_key_name] = document.getElementById('id_ch_name').value;
        cfg[__JRPC_key_band] =
            get_selected_option('id_ch_band', "Band");
        cfg[__JRPC_key_modulations] =
            get_selected_options('id_ch_mod', "Modulation");
        cfg[__JRPC_key_bitrates] =
            get_selected_options('id_ch_bps', "Bitrate");
        cfg[__JRPC_key_polarizations] =
            get_selected_options('id_ch_pol', "Polarization");
        cfg[__JRPC_key_bandwidths] =
            get_selected_options('id_ch_bw', "Bandwidth");

        return(cfg);

    }

    function get_selected_option(select_id, option)
    {
        var x = document.getElementById(select_id).selectedIndex;
        var v = document.getElementsByTagName("option")[x].value;
        if ( v == null ) { throw "Must made a selection for = " + option; }
        return(v);
    }

    function get_selected_options(select_id, option)
    {

        var r = [];
        var options = document.getElementById(select_id).options;

        for (var i = 0, s_len = options.length; i < s_len; i++) {
            var o  = options[i];
            if (o.selected) { r.push(o.value); }
        }

        if ( r.length == 0 )
            { throw "Must selection an option for " + option; }

        return r;
    }

    function verify_channel_name(textarea_id)
    {

        var e = document.getElementById(textarea_id);
        var name = e.value;
        if ( name == __NAME_initial_value ) { name = ''; }

        // 1) length check
        if ( name.length == 0 ) { alert('Name cannot be empty'); return; }

        // 2) REGEX match
        if ( __REGEX_name.exec(name) == null )
            { alert('Wrong channel name format.'); return; }

        // 3) uniqueness check
        var jrc = new $.JsonRpcClient({ ajaxUrl: '/jrpc/' });
        jrc.call(
            'configuration.gs.channel.uniqueIdentifier', [ name ],
            function(result) {
                if ( result == true )
                    { alert('Channel name already exists.'); }
            },
            function(error) { __error(error['message']); }
        );

    }

    function init_textarea(textarea_id) {

        var e = document.getElementById(textarea_id);
        e.value = __NAME_initial_value;
        e.className = 'textarea-initial';

    }

    function erase_textarea(textarea_id) {

        var e = document.getElementById(textarea_id);
        var name = e.value;
        if ( ( name != __NAME_initial_value) && ( name != '' ) )
            { return; }

        e.value = '';
        e.className = '';

    }

    function clean_textarea(textarea_id) {

        var e = document.getElementById(textarea_id);
        var ch_name = e.value;
        var matches = __REGEX_name.exec(ch_name);

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

    function __error(msg) {
        if ( __DEBUG__ ) console.log(msg);
        alert(msg);
    }
