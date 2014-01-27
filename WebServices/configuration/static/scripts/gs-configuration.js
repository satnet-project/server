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

var __TMP_JRPC_gs_id = '';
var __TMP_JRPC_ch_id = '';

    // Event binding to handlers
    $(document).ready(function() {
        add_components();
        $( "#add_channel_button" )
            .on("click", add_channel_dialog_init);
        $( "#add_channel_dialog_add_button" )
            .on("click", add_channel_dialog_add);
        $( "#add_channel_dialog_cancel_button" )
            .on("click", add_channel_dialog_hide);
    });

    function add_components() {
        adapt_gs_buttons();
        adapt_channel_buttons();
    }

    function adapt_gs_buttons() {
        $('#edit-gs-button').puibutton({
            icon: 'ui-icon-scissors',
            text: 'Edit',
            click: function() {
                var gs_id = $(this).attr('data-gs-id');
                console.log('Edit ground station, gs_id = ' + gs_id);
                //edit_gs(gs_id);
            }
        });
        $('#delete-gs-button').puibutton({
            icon: 'ui-icon-close',
            text: 'Delete',
            click: function() {
                var gs_id = $(this).attr('data-gs-id');
                console.log('Delete ground station, gs_id = ' + gs_id);
                //delete_gs(gs_id);
            }
        });
        $('#add-ch-button').puibutton({
            icon: 'ui-icon-newwin',
            text: '(+) channel',
            click: function() {
                var gs_id = $(this).attr('data-gs-id');
                console.log('Add channel to ground station, gs_id = ' + gs_id);
                add_channel_dialog_init();
            }
        });
    }

    function adapt_channel_buttons() {
        var edit_ch_buttons = document
                .getElementsByClassName('edit-ch');
        for(var i = 0; i < edit_ch_buttons.length; i++) {
            var e_b = edit_ch_buttons[i].id;
            console.log('Adapting button_id = ' + e_b);
            add_edit_channel_components(e_b);
        }
        var delete_ch_buttons = document
                .getElementsByClassName('delete-ch');
        for(i = 0; i < delete_ch_buttons.length; i++) {
            e_b = delete_ch_buttons[i].id;
            console.log('Adapting button_id = ' + e_b);
            add_delete_channel_components(e_b);
        }
    }

    function add_edit_channel_components(button_id) {
        $( "#" + button_id ).puibutton({
            icon: 'ui-icon-scissors',
            text: 'Edit',
            click: function() {
                var channel_id = $(this).attr('data-ch-id');
                var gs_id = $(this).attr('data-gs-id');
                console.log('Edit channel, id = ' + channel_id +
                                                    'gs_id = ' + gs_id);
                edit_channel_dialog_init(gs_id, channel_id);
            }
        });
    }

    function add_delete_channel_components(button_id) {
        console.log('Adapting button_id = ' + button_id);
        $( "#" + button_id ).puibutton({
            icon: 'ui-icon-close',
            text: 'Delete',
            click: function() {
                var channel_id = $(this).attr('data-ch-id');
                var gs_id = $(this).attr('data-gs-id');
                console.log('Delete channel, id = ' + channel_id +
                                                    'gs_id = ' + gs_id);
                delete_channel(gs_id, channel_id);
                window.location.reload(true);
            }
        });
    }

    function delete_channel(gs_id, channel_id) {
        new $.JsonRpcClient({ ajaxUrl: '/jrpc/' }).call(
            'configuration.gs.channel.delete', [ gs_id, channel_id ],
            function(result) {
                console.log('Channel deleted succesfully!');
                alert('Channel deleted succesfully!');
            },
            function(error) { __error(error['message']); }
        );
    }

    function add_channel_dialog_load() {
        init_textarea('id_ch_name');
        init_select_options('id_ch_mod');
        init_select_options('id_ch_band');
        init_select_options('id_ch_bps');
        init_select_options('id_ch_bw');
        init_select_options('id_ch_pol');
        __JRPC_get_options();
    }

    function edit_channel_dialog_load(gs_id, channel_id) {
        init_textarea('id_ch_name');
        init_select_options('id_ch_mod');
        init_select_options('id_ch_band');
        init_select_options('id_ch_bps');
        init_select_options('id_ch_bw');
        init_select_options('id_ch_pol');
        __JRPC_select_channel_cfg(gs_id, channel_id);
    }

    function add_channel_dialog_init() {
        add_channel_dialog_load();
        //$( "#add_channel_dialog" ).show();
        //$( "#add_channel_dialog_overlay" ).show();
    }

    function edit_channel_dialog_init(gs_id, channel_id) {
        edit_channel_dialog_load(gs_id, channel_id);
        //$( "#add_channel_dialog" ).show();
        //$( "#add_channel_dialog_overlay" ).show();
    }

    function add_channel_dialog_clean() {
        $( "#id_ch_name" ).value = '';
        clear_select_options('id_ch_mod');
        clear_select_options('id_ch_band');
        clear_select_options('id_ch_bps');
        clear_select_options('id_ch_bw');
        clear_select_options('id_ch_pol');
    }

    function add_channel_dialog_add() {
        var gs_id = $( "#add-ch-button" ).attr('data-gs-id');
        verify_channel_name('id_ch_name');
        try {
            var channel_cfg = create_channel_cfg(gs_id);
            if ( __DEBUG__ ) console.log(channel_cfg);
            new $.JsonRpcClient({ ajaxUrl: '/jrpc/' }).call(
                'configuration.gs.channel.create', [ channel_cfg ],
                function(result) {
                    console.log('Channel created succesfully!');
                    alert('Channel created succesfully!');
                    add_channel_dialog_hide();
                },
                function(error) { __error(error['message']); }
            );
        }
        catch(err) { __error(err); }
    }

    function channel_dialog_show() {
        $( "#add_channel_dialog" ).show();
        $( "#add_channel_dialog_overlay" ).show();
    }

    function add_channel_dialog_hide() {
        $( "#add_channel_dialog" ).hide();
        $( "#add_channel_dialog_overlay" ).hide();
        add_channel_dialog_clean();
    }

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

    function clear_select_options(select_id) {
        console.log('>>>> clear_select_options for e.id = ' + select_id);
        print_select_options(select_id);
        var e = document.getElementById(select_id);
        for (var i = e.options.length; i > 0; i--)
            { e.options[i-1] = null; }
        print_select_options(select_id);
    }

    function print_select_options(select_id) {
        var e = document.getElementById(select_id);
        console.log('>>> options for e.id = ' + select_id);
        for (var i = 0; i < e.options.length; i++)
            { console.log('o[' + i + ']' + e.options[i].text); }
    }

    function channel_dialog_show_options()
    {
        console.log('############### options BEGIN');
        print_select_options('id_ch_mod');
        print_select_options('id_ch_bw');
        print_select_options('id_ch_bps');
        print_select_options('id_ch_pol');
        console.log('############### options END');
    }

    function __JRPC_get_options() {
        new $.JsonRpcClient({ ajaxUrl: '/jrpc/' }).call(
            'configuration.gs.channel.getOptions', [],
            function(result){
                console.log('configuration.gs.channel.getOptions');
                console.log(result);
                process_channel_options(result);
                channel_dialog_show();
            },
            function(error) { __error(error['message']); }
        );
    }

    function __JRPC_select_channel_cfg(gs_id, channel_id) {
        __TMP_JRPC_gs_id = gs_id;
        __TMP_JRPC_ch_id = channel_id;
        new $.JsonRpcClient({ ajaxUrl: '/jrpc/' }).call(
            'configuration.gs.channel.getOptions', [],
            function(result, gs_id, channel_id) {
                console.log('configuration.gs.channel.getOptions');
                console.log(result);
                process_channel_options(result);
                new $.JsonRpcClient({ ajaxUrl: '/jrpc/' }).call(
                    'configuration.gs.channel.getConfiguration',
                        [__TMP_JRPC_gs_id, __TMP_JRPC_ch_id],
                    function(result) {
                        console.log('configuration.gs.channel.getConfiguration');
                        console.log(result);
                        process_channel_selections(result);
                        channel_dialog_show(result);
                },
                function(error) { __error(error['message']); }
        );
            },
            function(error) { __error(error['message']); }
        );
    }

    function process_channel_options(result) {
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

    function process_channel_selections(result) {
        init_ch_name('id_ch_name', result[__JRPC_key_name]);
        select_options('id_ch_mod', result[__JRPC_key_modulations]);
        select_options('id_ch_band', result[__JRPC_key_band]);
        select_options('id_ch_bps', result[__JRPC_key_bitrates]);
        select_options('id_ch_bw', result[__JRPC_key_bandwidths]);
        select_options('id_ch_pol', result[__JRPC_key_polarizations]);
    }

    function __JRPC_select_channel_options(gs_id, channel_id) {
        new $.JsonRpcClient({ ajaxUrl: '/jrpc/' }).call(
            'configuration.gs.channel.getConfiguration', [gs_id, channel_id],
            function(result, gs_id, channel_id) {
                console.log('configuration.gs.channel.getConfiguration');
                console.log(result);
                process_channel_selections(result);
            },
            function(error) { __error(error['message']); }
        );
    }

    function init_ch_name(textarea_id, name)
    {
        var e = document.getElementById(textarea_id);
        e.value = name;
        e.style.color = 'green';
        e.style.fontWeight = '';
        e.style.fontStyle = '';
    }

    function select_options(component_id, selections) {
        var select = document.getElementById(component_id);
        for ( var i = 0, l = select.options.length, o; i < l; i++ ) {
            o = select.options[i];
            for ( var j = 0, s; j < selections.length; j++ ) {
                s = selections[j];
                if ( s.toString(10) == o.text ) { o.selected = true; }
            }
        }
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

    function get_selected_option(select_id, option) {
        var x = document.getElementById(select_id).selectedIndex;
        var v = document.getElementsByTagName("option")[x].value;
        if ( v == null ) { throw "Must made a selection for = " + option; }
        return(v);
    }

    function get_selected_options(select_id, option) {
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

    function verify_channel_name(textarea_id) {
        var e = document.getElementById(textarea_id);
        var name = e.value;
        if ( name == __NAME_initial_value ) { name = ''; }

        // 1) length check
        if ( name.length == 0 ) { alert('Name cannot be empty'); return; }
        // 2) REGEX match
        if ( __REGEX_name.exec(name) == null )
            { alert('Wrong channel name format.'); return; }

        // 3) uniqueness check
        new $.JsonRpcClient({ ajaxUrl: '/jrpc/' }).call(
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
        if ( ( name != __NAME_initial_value) && ( name != '' ) ) { return; }
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

    function __error(msg) {if(__DEBUG__)console.log(msg);alert(msg);}
