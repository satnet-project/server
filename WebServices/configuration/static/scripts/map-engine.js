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

    var __DEBUG__ = true;
    var __ZOOM__ = 10;
    var __ZOOM_STEP__ = 3;
    var __ZOOM_SEARCH__ = 13;
    var __MARKER_MSG__ = "<center><b>Move me or search!<br/>(";
    var options_osmGeocoder = {
        collapsed: true,
        position: 'topright',
        text: 'Locate',
        bounds: null,
        email: null,
        callback: __geocoder_result
    };
    var osmGeocoder = new L.Control.OSMGeocoder(options_osmGeocoder);
    var options_coordinates = {
        position:"bottomleft",
        decimals: 4,
        decimalSeperator: ".",
        labelTemplateLat: "Latitude: {y}",
        labelTemplateLng: "Longitude: {x}",
        enableUserInput: false,
        useDMS: false,
        useLatLngOrder: true
    };
    var coordinates = L.control.coordinates(options_coordinates);
    
    var gs_location_marker;
    var __my_map;
    var __my_map_options;

    function __marker_drag_end(e) {
        if ( e == null ) return;
        
        var d_lat = e.target.getLatLng()['lat'];
        var d_lng = e.target.getLatLng()['lng'];
    
        if (__DEBUG__)
            console.log("__marker_drag_end, to = ("
                            + d_lat + ", " + d_lng + ")");
    
        move_marker(gs_location_marker, d_lat, d_lng);
        save_position(d_lat, d_lng);
    } 

    function __startup_map(map, options)
        { __init_map(map, options); __load_map()}

    function __init_map(map, options) {
        __my_map = map;     // save reference to main map
        __my_map_options = options;
        if (__DEBUG__) console.log('map initialized!')
    }

    function __load_map() {
        // plugins
        __my_map.addControl(osmGeocoder);
        __my_map.addControl(coordinates);
        
        var lat = $( '#id_latitude' ).prop('value');
        var lng = $( '#id_longitude' ).prop('value');
    
        if ( __DEBUG__ )
            console.log('lat = ' + lat + ', lng = ' + lng);
        __my_map.setView(new L.LatLng(lat, lng), __ZOOM__);

        gs_location_marker = L.marker([0, 0], { draggable: 'true' });
        gs_location_marker.addTo(__my_map);
        move_marker(gs_location_marker, lat, lng);
        save_position(lat, lng);

        gs_location_marker.on('dragend', __marker_drag_end);
    }

    function __init_operations_map(map, options) {
        __my_map = map;     // save reference to main map
        var lat = $( '#id_latitude' ).prop('value');
        var lng = $( '#id_longitude' ).prop('value');
    
        if ( __DEBUG__ ) console.log('lat = ' + lat + ', lng = ' + lng);
        map.setView(new L.LatLng(lat, lng), __ZOOM__);

        gs_location_marker = L.marker([0, 0], { draggable: 'true' });
        gs_location_marker.addTo(map);
        move_marker(gs_location_marker, lat, lng);
        save_position(lat, lng);

        gs_location_marker.on('dragend', __marker_drag_end);
    }
    
    function __geocoder_result(results) {
    
        if ( ( results == null ) || ( results.length == 0 ) )
            { geocoder_no_results(); }
        
        var r_lat = results[0]['lat'];
        var r_lng = results[0]['lon'];  // osm geocoder api: 'lon', not 'lng'

        if ( __DEBUG__ )
            console.log("__geocoder_result, (" + r_lat + ", " + r_lng + ")");
        
        move_marker(gs_location_marker, r_lat, r_lng);
        __my_map.zoomIn(__ZOOM_STEP__);
        save_position(r_lat, r_lng);

    }
  
    function geocoder_no_results() {
        if ( __DEBUG__ ) console.log("No results found!");
        alert("No results found!");
    }
    
    function move_marker(m, lat, lng) {
        __my_map.setView([lat, lng]);
        m   .setLatLng([lat, lng])
            .bindPopup(__MARKER_MSG__ + myRound(lat, 2) + "," + myRound(lng, 2) 
                            + ")</center></b>")
            .openPopup()
            .dragging.enable();
    }

    function save_position(lat, lng) {
        $( "#id_latitude" ).attr("value", lat);
        $( "#id_longitude" ).attr("value", lng);
    }

    function myRound(value, places) {
        var multiplier = Math.pow(10, places);
        return (Math.round(value * multiplier) / multiplier);
    }
    
