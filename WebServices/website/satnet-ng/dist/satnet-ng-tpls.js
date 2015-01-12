angular.module('satnet-ui').run(['$templateCache', function($templateCache) {
  'use strict';

  $templateCache.put('templates/addGroundStation.html',
    "<div class=\"modal-header\"><h3 class=\"modal-title\">Add Ground Station</h3></div><div class=\"modal-body\" style=\"display: table-row\"><div style=\"float: left; display: table-cell; width: 175px; margin: 15px\"><form name=\"form\"><div class=\"control-group\" ng-class=\"{ 'has-error': form.identifier.$invalid }\"><label class=\"control-label\" for=\"identifier\">Identifier</label><input type=\"text\" name=\"identifier\" class=\"form-control\" style=\"width: 95%\" ng-model=\"gs.identifier\" ng-remote-validate=\"/configuration/groundstations/valid_id\" ng-remote-throttle=\"200\" ng-remote-method=\"GET\" ng-pattern=\"/^[a-zA-Z0-9.\\-_]{5,8}$/\" required></div><div class=\"control-group\" ng-class=\"{ 'has-error': form.callsign.$invalid }\"><label class=\"control-label\" for=\"callsign\">Callsign</label><input type=\"text\" name=\"callsign\" ng-model=\"gs.callsign\" class=\"form-control\" style=\"width: 95%\" ng-pattern=\"/^[a-zA-Z0-9]{3,8}$/\" required></div><div class=\"control-group\" ng-class=\"{ 'has-error': form.elevation.$invalid }\"><label class=\"control-label\" for=\"elevation\">Min. Antenna Elevation</label><input type=\"number\" name=\"elevation\" ng-model=\"gs.elevation\" class=\"form-control\" style=\"width: 95%\" step=\"0.01\" min=\"0\" max=\"90\" required></div><hr><label for=\"add_gs_lat\">Latitude</label><input type=\"text\" name=\"add_gs_lat\" readonly ng-model=\"markers.gs.lat\" style=\"width: 95%\"><label for=\"add_gs_lng\">Longitude</label><input type=\"text\" name=\"add_gs_lng\" readonly ng-model=\"markers.gs.lng\" style=\"width: 95%\"></form></div><div style=\"display: table-cell\"><leaflet id=\"addGSMap\" style=\"float: left; width: 365px; height: 365px;\n" +
    "                 margin: 15px 15px 15px 0\" center=\"center\" markers=\"markers\" layers=\"layers\"></leaflet></div></div><div class=\"modal-footer\"><button class=\"btn btn-primary\" ng-click=\"ok()\" ng-disabled=\"form.$invalid\">(ok)</button> <button class=\"btn btn-warning\" ng-click=\"cancel()\">(cancel)</button></div>"
  );


  $templateCache.put('templates/addSpacecraft.html',
    "<div class=\"modal-header\"><h3 class=\"modal-title\">Add Spacecraft</h3></div><div class=\"modal-body\" style=\"display: inline-block\"><form name=\"form\"><div style=\"display: table-row; padding: 5px; margin: 5px\"><div style=\"display: table-cell; width: 300px\"><div class=\"control-group\" ng-class=\"{ 'has-error': form.identifier.$invalid }\"><label class=\"control-label\" for=\"identifier\">Identifier</label><input type=\"text\" name=\"identifier\" class=\"form-control\" style=\"width: 95%\" ng-model=\"sc.identifier\" ng-remote-validate=\"/configuration/spacecraft/valid_id\" ng-remote-throttle=\"200\" ng-remote-method=\"GET\" ng-pattern=\"/^[a-zA-Z0-9.\\-_]{5,8}$/\" required></div><div class=\"control-group\" ng-class=\"{ 'has-error': form.callsign.$invalid }\"><label class=\"control-label\" for=\"callsign\">Callsign</label><input type=\"text\" name=\"callsign\" ng-model=\"sc.callsign\" class=\"form-control\" style=\"width: 95%\" ng-pattern=\"/^[a-zA-Z0-9]{3,8}$/\" required></div></div><div style=\"display: table-cell; width: 300px\"><div class=\"control-group\" ng-class=\"{ 'has-error': form.tlegroup.$pristine }\"><div><label class=\"control-label\" for=\"tlegroup\">TLE Group (Celestrak)</label></div><div><ol id=\"tlegroup\" class=\"nya-bs-select\" ng-model=\"sc.tlegroup\" ng-change=\"groupChanged(sc.tlegroup)\"><li nya-bs-option=\"t in tlegroups group by t.section\"><span class=\"dropdown-header\">{{$group}}</span> <a>{{t.subsection}}</a></li></ol></div></div><div class=\"control-group\" ng-class=\"{ 'has-error': form.tleid.$pristine }\"><div><label class=\"control-label\" for=\"tleid\"><div style=\"display: table-row\"><div style=\"display: table-cell\"><span>TLE Id</span></div><div style=\"display: table-cell\" ng-show=\"sc.savedTleId\"><p style=\"font-size:70%\">(Current:{{ sc.savedTleId }})</p></div></div></label></div><div><ol id=\"tleid\" class=\"nya-bs-select\" ng-model=\"sc.tleid\" ng-disabled=\"sc.tlegroup\"><li nya-bs-option=\"t in tles\"><span class=\"dropdown-header\">{{$group}}</span> <a>{{t.spacecraft_tle_id}}</a></li></ol></div></div></div></div></form></div><div class=\"modal-footer\"><button class=\"btn btn-primary\" ng-click=\"ok()\" ng-disabled=\"form.$invalid\">(ok)</button> <button class=\"btn btn-warning\" ng-click=\"cancel()\">(cancel)</button></div>"
  );


  $templateCache.put('templates/editGroundStation.html',
    "<div class=\"modal-header\"><h3 class=\"modal-title\">Edit Ground Station</h3></div><div class=\"modal-body\" style=\"display: table-row\"><div style=\"float: left; display: table-cell; width: 175px; margin: 15px\"><form name=\"form\"><div class=\"control-group\" ng-class=\"{ 'has-error': form.identifier.$invalid }\"><label class=\"control-label\" for=\"identifier\">Identifier</label><input type=\"text\" name=\"identifier\" id=\"identifier\" class=\"form-control\" style=\"width: 95%\" ng-model=\"gs.identifier\" readonly></div><div class=\"control-group\" ng-class=\"{ 'has-error': form.callsign.$invalid }\"><label class=\"control-label\" for=\"callsign\">Callsign</label><input type=\"text\" name=\"callsign\" id=\"callsign\" ng-model=\"gs.callsign\" class=\"form-control\" style=\"width: 95%\" ng-pattern=\"/^[a-zA-Z0-9]{3,8}$/\" required></div><div class=\"control-group\" ng-class=\"{ 'has-error': form.elevation.$invalid }\"><label class=\"control-label\" for=\"elevation\">Min. Antenna Elevation</label><input type=\"number\" name=\"elevation\" id=\"elevation\" ng-model=\"gs.elevation\" class=\"form-control\" style=\"width: 95%\" step=\"0.01\" min=\"0\" max=\"90\" required></div><hr><label for=\"edit_gs_lat\">Latitude</label><input type=\"text\" name=\"edit_gs_lat\" id=\"edit_gs_lat\" readonly ng-model=\"markers.gs.lat\" style=\"width: 95%\"><label for=\"edit_gs_lng\">Longitude</label><input type=\"text\" name=\"edit_gs_lng\" id=\"edit_gs_lng\" readonly ng-model=\"markers.gs.lng\" style=\"width: 95%\"> <input type=\"hidden\" name=\"hidden_lat\" ng-model=\"markers.gs.lat\"> <input type=\"hidden\" name=\"hidden_lng\" ng-model=\"markers.gs.lng\"></form></div><div style=\"display: table-cell\"><leaflet id=\"editGSMap\" style=\"float: left; width: 365px; height:365px; margin: 15px 15px 15px 0px\" markers=\"markers\" center=\"center\" layers=\"layers\"></leaflet></div></div><div class=\"modal-footer\"><button class=\"btn btn-primary\" ng-click=\"update()\" ng-disabled=\"form.$pristine || form.$invalid\">(update)</button> <button class=\"btn btn-warning\" ng-click=\"cancel()\">(cancel)</button> <button class=\"btn btn-danger\" ng-click=\"erase()\">(remove)</button></div>"
  );


  $templateCache.put('templates/editSpacecraft.html',
    "<div class=\"modal-header\"><h3 class=\"modal-title\">Edit Spacecraft</h3></div><div class=\"modal-body\" style=\"display: inline-block\"><form name=\"form\"><div style=\"display: inline-block; padding: 20px\"><div style=\"float: left; width: 250px\"><div class=\"control-group\" ng-class=\"{ 'has-error': form.identifier.$invalid }\"><label class=\"control-label\" for=\"identifier\">Identifier</label><input type=\"text\" name=\"identifier\" class=\"form-control\" style=\"width: 95%\" ng-model=\"sc.identifier\" readonly></div><div class=\"control-group\" ng-class=\"{ 'has-error': form.callsign.$invalid }\"><label class=\"control-label\" for=\"callsign\">Callsign</label><input type=\"text\" name=\"callsign\" ng-model=\"sc.callsign\" class=\"form-control\" style=\"width: 95%\" ng-pattern=\"/^[a-zA-Z0-9]{3,8}$/\" required></div></div><div class=\"my-tle-menu\"><div class=\"control-group\" ng-class=\"{ 'has-error': form.tlegroup.$pristine }\"><label class=\"control-label\" for=\"tlegroup\">TLE Group (Celestrak)</label><ol id=\"tlegroup\" class=\"nya-bs-select\" ng-model=\"sc.tlegroup\" ng-change=\"groupChanged(sc.tlegroup)\"><li nya-bs-option=\"t in tlegroups group by t.section\"><span class=\"dropdown-header\">{{$group}}</span> <a>{{t.subsection}}</a></li></ol></div><div class=\"control-group\" ng-class=\"{ 'has-error': form.tleid.$pristine }\"><label class=\"control-label\" for=\"tleid\"><div style=\"display: inline-block\"><div style=\"float: left, padding: 20px\"><p>TLE Id</p></div><div><p style=\"font-size:70%\">(Current: {{ sc.savedTleId }})</p></div></div></label><ol id=\"tleid\" class=\"nya-bs-select\" ng-model=\"sc.tleid\"><li nya-bs-option=\"t in tles\"><span class=\"dropdown-header\">{{$group}}</span> <a>{{t.spacecraft_tle_id}}</a></li></ol></div></div></div></form></div><div class=\"modal-footer\"><button class=\"btn btn-primary\" ng-click=\"update()\" ng-disabled=\"form.$invalid\">(update)</button> <button class=\"btn btn-warning\" ng-click=\"cancel()\">(cancel)</button> <button class=\"btn btn-danger\" ng-click=\"erase()\">(remove)</button></div>"
  );


  $templateCache.put('templates/leop/manageCluster.html',
    "<div class=\"modal-header\"><h3 class=\"modal-title\">Manage Cluster ({{ cluster.identifier }})</h3></div><style>label.control-label { font-size: 85%; }</style><div class=\"modal-body\" style=\"display: inline-block; width: 100%\"><form name=\"form\"><div style=\"display: table; table-layout: fixed; border-spacing: 5px; width: 100%\"><div class=\"right-border\" style=\"display: table-cell; width: 30%\"><div><h4>Cluster TLE</h4></div><div class=\"control-group\" ng-class=\"{ 'has-error': form.tle_l1.$invalid }\"><label class=\"control-label\" for=\"tle_l1\">First line</label><input type=\"text\" name=\"tle_l1\" class=\"form-control\" style=\"width: 100%\" ng-model=\"cluster.tle.l1\" ng-pattern=\"/^[a-zA-Z0-9.\\s-]{69}$/\" required></div><div class=\"control-group\" ng-class=\"{ 'has-error': form.tle_l2.$invalid }\"><label class=\"control-label\" for=\"tle_l2\">Second line</label><input type=\"text\" name=\"tle_l2\" class=\"form-control\" style=\"width: 100%\" ng-model=\"cluster.tle.l2\" ng-pattern=\"/^[a-zA-Z0-9.\\s-]{69}$/\" required></div></div><div style=\"display: table-cell; width: 20px\"></div><div style=\"display: table-cell; width: 60%\"><!--<div>--><div style=\"display: table-cell\"><h4>UFO Objects</h4></div><div ng-hide=\"cluster.ufos.length\"><p class=\"no-items\">(no ufos)</p></div><div ng-repeat=\"u in cluster.ufos\"><div class=\"ufos-item\"><a class=\"link action-link\" ng-click=\"identify(u.object_id)\">Object #{{ u.object_id }}</a></div><div class=\"ufos-item\"><span></span></div></div><div style=\"display: table-row\"><div style=\"display: table-cell; font-size: 75%\"><a class=\"green-link\" ng-show=\"cluster.ufos.length < cluster.max_ufos\" ng-click=\"add()\">(+ add)</a> <a class=\"red-link\" ng-hide=\"cluster.ufos.length < cluster.max_ufos\">MAXIMUM</a></div><div ng-show=\"cluster.ufos.length\"><a class=\"red-link action-link\" ng-click=\"remove()\">(- remove)</a></div></div><hr><!--</div>--><!--\n" +
    "            <div><h4>Identified Objects</h4></div>\n" +
    "            <div ng-hide=\"cluster.identified.length\"><p class='no-items'>(none identified)</p></div>\n" +
    "                <ol class='unsalted-list'>\n" +
    "                <li class='ufo-item' ng-repeat=\"i in cluster.identified\">\n" +
    "                    <div class=\"bottom-cell\">\n" +
    "                    <div style='display: table-row'>\n" +
    "                        <div style='display: table-cell'>\n" +
    "                            <h4>Object #{{ i.object_id }}</h4>\n" +
    "                            <a class='link action-link' ng-click=\"save(i.object_id)\">(save)</a>\n" +
    "                            <a class='link action-link' ng-click=\"cancel(i.object_id)\">(cancel)</a>\n" +
    "                            <a class='link action-link' ng-click=\"forget(i.object_id)\">(forget)</a>\n" +
    "                        </div>\n" +
    "                        <div class='control-group' style='display: table-cell'\n" +
    "                            ng-class=\"{ 'has-error': form.i_alias.$invalid }\">\n" +
    "                            <label class='control-label' for='i_alias'>Alias</label>\n" +
    "                            <input type='text' name='i_alias'\n" +
    "                                class='form-control' style='width: 100%'\n" +
    "                                ng-model=\"i.alias\"\n" +
    "                                ng-pattern='/^[a-zA-Z0-9]{3,8}$/'\n" +
    "                                required />\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "                    <div style='display: table-row'>\n" +
    "\n" +
    "                        <div style='display: table-cell'>\n" +
    "                            <div class='control-group'\n" +
    "                                ng-class=\"{ 'has-error': form.i_tle_l1.$invalid }\">\n" +
    "                                <label class='control-label' for='i_tle_l1'>First line</label>\n" +
    "                                <input type='text' name='i_tle_l1'\n" +
    "                                    class='form-control' style='width: 100%'\n" +
    "                                    ng-model=\"i.tle.l1\"\n" +
    "                                    ng-pattern='/^[a-zA-Z0-9.\\s-]{69}$/'\n" +
    "                                    required />\n" +
    "                            </div>\n" +
    "                        </div>\n" +
    "                        <div style='display: table-cell'>\n" +
    "                            <div class='control-group'\n" +
    "                                ng-class=\"{ 'has-error': form.i_tle_l2.$invalid }\">\n" +
    "                                <label class='control-label' for='i_tle_l2'>Second line</label>\n" +
    "                                <input type='text' name='i_tle_l2'\n" +
    "                                    class='form-control' style='width: 100%'\n" +
    "                                    ng-model=\"i.tle.l2\"\n" +
    "                                    ng-pattern='/^[a-zA-Z0-9.\\s-]{69}$/'\n" +
    "                                    required />\n" +
    "                            </div>\n" +
    "                        </div>\n" +
    "\n" +
    "                    </div>\n" +
    "                    </div>\n" +
    "                </li>\n" +
    "                </ol>\n" +
    "                       --></div></div></form></div><div class=\"modal-footer\"><button class=\"btn btn-primary\" ng-click=\"ok()\" ng-disabled=\"form.$invalid\">(ok)</button> <button class=\"btn btn-warning\" ng-click=\"cancel()\">(cancel)</button></div>"
  );


  $templateCache.put('templates/leop/manageGroundStations.html',
    "<div class=\"modal-header\"><h3 class=\"modal-title\">Manage Ground Stations</h3></div><div class=\"modal-body\" style=\"display: table-row\"><form name=\"form\"><div style=\"width: 300px; display: table-cell; text-align: center\"><h4>Available GS</h4><select multiple ng-model=\"gsIds.aItems\" ng-options=\"aid as aid.groundstation_id for aid in gsIds.leop_gs_available\" style=\"width: 95%\" class=\"leop-gs-duallist\"></select></div><div style=\"width: 10px; display: table-cell; margin-top: 50px\"><button id=\"a2u\" class=\"btn\" ng-disabled=\"!gsIds.aItems.length\" ng-click=\"selectGs()\">&gt;</button> <button id=\"u2a\" class=\"btn\" ng-disabled=\"!gsIds.uItems.length\" ng-click=\"unselectGs()\">&lt;</button></div><div style=\"width: 300px; display: table-cell; text-align: center\"><h4>Choosen GS</h4><select multiple ng-model=\"gsIds.uItems\" ng-options=\"uid as uid.groundstation_id for uid in gsIds.leop_gs_inuse\" style=\"width: 95%\"></select></div></form></div><div class=\"modal-footer\"><button class=\"btn btn-primary\" ng-click=\"ok()\"><!--ng-disabled=\"!gsIds.toAdd || !gsIds.toRemove\">-->(ok)</button> <button class=\"btn btn-warning\" ng-click=\"cancel()\">(cancel)</button></div>"
  );


  $templateCache.put('templates/notifier/logNotifier.html',
    "<input type=\"checkbox\" name=\"n-area-toggle\" id=\"n-area-toggle\"><div ng-controller=\"logNotifierCtrl\" class=\"n-area\"><div class=\"n-area-title\"><label for=\"n-area-toggle\"></label></div><div class=\"n-area-content\"><ul class=\"n-area-list\"><li ng-repeat=\"e in eventLog\"><div class=\"n-area-info-row\"><div class=\"n-area-type-cell\"><p class=\"{{ e.type }}\">[@{{ e.timestamp }}]</p></div><div class=\"n-area-content-cell\"><span class=\"{{ e.type }}\">{{ e.msg }}</span></div></div></li></ul></div></div>"
  );

}]);
