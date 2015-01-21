angular.module('satnet-ui').run(['$templateCache', function($templateCache) {
  'use strict';

  $templateCache.put('templates/addGroundStation.html',
    "<div class=\"modal-header\"><h3 class=\"modal-title\">Add Ground Station</h3></div><div class=\"modal-body\" style=\"display: table-row\"><div style=\"float: left; display: table-cell; width: 175px; margin: 15px\"><form name=\"form\"><div class=\"control-group\" ng-class=\"{ 'has-error': form.identifier.$invalid }\"><label class=\"control-label\" for=\"identifier\">Identifier</label><input type=\"text\" name=\"identifier\" class=\"form-control\" style=\"width: 95%\" ng-model=\"gs.identifier\" ng-remote-validate=\"/configuration/groundstations/valid_id\" ng-remote-throttle=\"200\" ng-remote-method=\"GET\" ng-pattern=\"/^[a-zA-Z0-9.\\-_]{5,8}$/\" required></div><div class=\"control-group\" ng-class=\"{ 'has-error': form.callsign.$invalid }\"><label class=\"control-label\" for=\"callsign\">Callsign</label><input type=\"text\" name=\"callsign\" ng-model=\"gs.callsign\" class=\"form-control\" style=\"width: 95%\" ng-pattern=\"/^[a-zA-Z0-9]{3,8}$/\" required></div><div class=\"control-group\" ng-class=\"{ 'has-error': form.elevation.$invalid }\"><label class=\"control-label\" for=\"elevation\">Min. Antenna Elevation</label><input type=\"number\" name=\"elevation\" ng-model=\"gs.elevation\" class=\"form-control\" style=\"width: 95%\" step=\"0.01\" min=\"0\" max=\"90\" required></div><hr><label for=\"add_gs_lat\">Latitude</label><input type=\"text\" name=\"add_gs_lat\" readonly ng-model=\"markers.gs.lat\" style=\"width: 95%\"><label for=\"add_gs_lng\">Longitude</label><input type=\"text\" name=\"add_gs_lng\" readonly ng-model=\"markers.gs.lng\" style=\"width: 95%\"></form></div><div style=\"display: table-cell\"><leaflet id=\"addGSMap\" style=\"float: left; width: 365px; height: 365px;\n" +
    "                 margin: 15px 15px 15px 0\" center=\"center\" markers=\"markers\" layers=\"layers\"></leaflet></div></div><div class=\"modal-footer\"><button class=\"btn btn-primary\" ng-click=\"ok()\" ng-disabled=\"form.$invalid\">(ok)</button> <button class=\"btn btn-warning\" ng-click=\"cancel()\">(cancel)</button></div>"
  );


  $templateCache.put('templates/addSpacecraft.html',
    "<div class=\"modal-header\"><h3 class=\"modal-title\">Add Spacecraft</h3></div><div class=\"modal-body\" style=\"display: inline-block\"><form name=\"form\"><div style=\"display: table-row; padding: 5px; margin: 5px\"><div style=\"display: table-cell; width: 300px\"><div class=\"control-group\" ng-class=\"{ 'has-error': form.identifier.$invalid }\"><label class=\"control-label\" for=\"identifier\">Identifier</label><input type=\"text\" name=\"identifier\" class=\"form-control\" style=\"width: 95%\" ng-model=\"sc.identifier\" ng-remote-validate=\"/configuration/spacecraft/valid_id\" ng-remote-throttle=\"200\" ng-remote-method=\"GET\" ng-pattern=\"/^[a-zA-Z0-9.\\-_]{5,8}$/\" required></div><div class=\"control-group\" ng-class=\"{ 'has-error': form.callsign.$invalid }\"><label class=\"control-label\" for=\"callsign\">Callsign</label><input type=\"text\" name=\"callsign\" ng-model=\"sc.callsign\" class=\"form-control\" style=\"width: 95%\" ng-pattern=\"/^[a-zA-Z0-9]{3,8}$/\" required></div></div><div style=\"display: table-cell; width: 300px\"><div class=\"control-group\" ng-class=\"{ 'has-error': form.tlegroup.$pristine }\"><div><label class=\"control-label\" for=\"tlegroup\">TLE Group (Celestrak)</label></div><div><ol id=\"tlegroup\" class=\"nya-bs-select\" ng-model=\"sc.tlegroup\" ng-change=\"groupChanged(sc.tlegroup)\"><li nya-bs-option=\"t in tlegroups group by t.section\"><span class=\"dropdown-header\">{{$group}}</span> <a>{{t.subsection}}</a></li></ol></div></div><div class=\"control-group\" ng-class=\"{ 'has-error': form.tleid.$pristine }\"><div><label class=\"control-label\" for=\"tleid\"><div style=\"display: table-row\"><div style=\"display: table-cell\"><span>TLE Id</span></div><div style=\"display: table-cell\" ng-show=\"sc.savedTleId\"><p style=\"font-size:70%\">(Current:{{ sc.savedTleId }})</p></div></div></label></div><div><ol id=\"tleid\" class=\"nya-bs-select\" ng-model=\"sc.tleid\" ng-disabled=\"sc.tlegroup\"><li nya-bs-option=\"t in tles\"><span class=\"dropdown-header\">{{$group}}</span> <a>{{t.spacecraft_tle_id}}</a></li></ol></div></div></div></div></form></div><div class=\"modal-footer\"><button class=\"btn btn-primary\" ng-click=\"ok()\" ng-disabled=\"form.$invalid\">(ok)</button> <button class=\"btn btn-warning\" ng-click=\"cancel()\">(cancel)</button></div>"
  );


  $templateCache.put('templates/countdown/countdown.html',
    "<div ng-controller=\"countdownCtrl\" style=\"width:100%\" ng-click=\"toggle()\" class=\"countdown\"><div><div ng-show=\"cd.expired\"><p>{{ cd.label }}</p></div><div ng-hide=\"cd.expired || cd.hide\"><p>{{ cd.diff | cdDate }}</p></div></div></div>"
  );


  $templateCache.put('templates/editGroundStation.html',
    "<div class=\"modal-header\"><h3 class=\"modal-title\">Edit Ground Station</h3></div><div class=\"modal-body\" style=\"display: table-row\"><div style=\"float: left; display: table-cell; width: 175px; margin: 15px\"><form name=\"form\"><div class=\"control-group\" ng-class=\"{ 'has-error': form.identifier.$invalid }\"><label class=\"control-label\" for=\"identifier\">Identifier</label><input type=\"text\" name=\"identifier\" id=\"identifier\" class=\"form-control\" style=\"width: 95%\" ng-model=\"gs.identifier\" readonly></div><div class=\"control-group\" ng-class=\"{ 'has-error': form.callsign.$invalid }\"><label class=\"control-label\" for=\"callsign\">Callsign</label><input type=\"text\" name=\"callsign\" id=\"callsign\" class=\"form-control\" style=\"width: 95%\" ng-pattern=\"/^[a-zA-Z0-9]{3,8}$/\" ng-model=\"gs.callsign\" required><!--  --></div><div class=\"control-group\" ng-class=\"{ 'has-error': form.elevation.$invalid }\"><label class=\"control-label\" for=\"elevation\">Min. Antenna Elevation</label><input type=\"number\" name=\"elevation\" id=\"elevation\" ng-model=\"gs.elevation\" class=\"form-control\" style=\"width: 95%\" step=\"0.01\" min=\"0\" max=\"90\" required></div><hr><div class=\"control-group\" ng-class=\"{ 'has-error': form.edit_gs_lat.$invalid }\"><label for=\"edit_gs_lat\">Latitude</label><input name=\"edit_gs_lat\" id=\"edit_gs_lat\" type=\"number\" step=\"0.01\" readonly ng-model=\"markers.gs.lat\" style=\"width: 95%\"></div><div class=\"control-group\" ng-class=\"{ 'has-error': form.edit_gs_lng.$invalid }\"><label for=\"edit_gs_lng\">Longitude</label><input name=\"edit_gs_lng\" id=\"edit_gs_lng\" type=\"number\" step=\"0.01\" readonly ng-model=\"markers.gs.lng\" style=\"width: 95%\"></div></form></div><div style=\"display: table-cell\"><leaflet id=\"editGSMap\" style=\"float: left; width: 365px; height:365px; margin: 15px 15px 15px 0px\" markers=\"markers\" center=\"center\" layers=\"layers\"></leaflet></div></div><div class=\"modal-footer\"><button class=\"btn btn-primary\" ng-click=\"update()\" ng-disabled=\"form.$pristine || form.$invalid\">(update)</button> <button class=\"btn btn-warning\" ng-click=\"cancel()\">(cancel)</button> <button class=\"btn btn-danger\" ng-click=\"erase()\">(remove)</button></div>"
  );


  $templateCache.put('templates/editSpacecraft.html',
    "<div class=\"modal-header\"><h3 class=\"modal-title\">Edit Spacecraft</h3></div><div class=\"modal-body\" style=\"display: inline-block\"><form name=\"form\"><div style=\"display: inline-block; padding: 20px\"><div style=\"float: left; width: 250px\"><div class=\"control-group\" ng-class=\"{ 'has-error': form.identifier.$invalid }\"><label class=\"control-label\" for=\"identifier\">Identifier</label><input type=\"text\" name=\"identifier\" class=\"form-control\" style=\"width: 95%\" ng-model=\"sc.identifier\" readonly></div><div class=\"control-group\" ng-class=\"{ 'has-error': form.callsign.$invalid }\"><label class=\"control-label\" for=\"callsign\">Callsign</label><input type=\"text\" name=\"callsign\" ng-model=\"sc.callsign\" class=\"form-control\" style=\"width: 95%\" ng-pattern=\"/^[a-zA-Z0-9]{3,8}$/\" required></div></div><div class=\"my-tle-menu\"><div class=\"control-group\" ng-class=\"{ 'has-error': form.tlegroup.$pristine }\"><label class=\"control-label\" for=\"tlegroup\">TLE Group (Celestrak)</label><ol id=\"tlegroup\" class=\"nya-bs-select\" ng-model=\"sc.tlegroup\" ng-change=\"groupChanged(sc.tlegroup)\"><li nya-bs-option=\"t in tlegroups group by t.section\"><span class=\"dropdown-header\">{{$group}}</span> <a>{{t.subsection}}</a></li></ol></div><div class=\"control-group\" ng-class=\"{ 'has-error': form.tleid.$pristine }\"><label class=\"control-label\" for=\"tleid\"><div style=\"display: inline-block\"><div style=\"float: left, padding: 20px\"><p>TLE Id</p></div><div><p style=\"font-size:70%\">(Current: {{ sc.savedTleId }})</p></div></div></label><ol id=\"tleid\" class=\"nya-bs-select\" ng-model=\"sc.tleid\"><li nya-bs-option=\"t in tles\"><span class=\"dropdown-header\">{{$group}}</span> <a>{{t.spacecraft_tle_id}}</a></li></ol></div></div></div></form></div><div class=\"modal-footer\"><button class=\"btn btn-primary\" ng-click=\"update()\" ng-disabled=\"form.$invalid\">(update)</button> <button class=\"btn btn-warning\" ng-click=\"cancel()\">(cancel)</button> <button class=\"btn btn-danger\" ng-click=\"erase()\">(remove)</button></div>"
  );


  $templateCache.put('templates/idle/timedoutDialog.html',
    "<div class=\"modal-header\"><h3>You've Timed Out!</h3></div><div class=\"modal-body\"><p>User has been idle for too long, logging out...</p></div>"
  );


  $templateCache.put('templates/idle/warningDialog.html',
    "<div class=\"modal-header\"><h3>User has been inactive for too long, session is about to expire.</h3></div><div class=\"modal-body\" ng-idle-countdown=\"countdown\" ng-init=\"countdown=5\"><p>Logging out in <span class=\"label label-warning\">{{countdown}}</span> <span ng-pluralize=\"\" count=\"countdown\" when=\"{'one': 'second', 'other': 'seconds' }\"></span></p><progressbar max=\"5\" value=\"countdown\" animate=\"true\" class=\"progress-striped active\" type=\"warning\"></div>"
  );


  $templateCache.put('templates/leop/manageCluster.html',
    "<div class=\"modal-header\"><h3 class=\"modal-title\">Manage Cluster ({{ cluster.identifier }})</h3></div><style>label.control-label { font-size: 85%; }</style><div class=\"modal-body\" style=\"display: inline-block; width: 100%\"><form name=\"form\"><div style=\"display: table; table-layout: fixed; border-spacing: 5px; width: 100%\"><div class=\"right-border\" style=\"display: table-cell; width: 200px\"><div><h4>Launch Date (UTC)</h4><div class=\"dropdown\"><a class=\"dropdown-toggle my-toggle-select\" id=\"dLabel\" role=\"button\" data-toggle=\"dropdown\" data-target=\"#\" href=\"\"><div class=\"input-append\"><input type=\"text\" class=\"input-large\" ng-disabled=\"!cluster.edit\" data-ng-model=\"cluster.date\"> <span class=\"add-on\"><i class=\"icon-calendar\"></i></span></div></a><ul class=\"dropdown-menu\" role=\"menu\" aria-labelledby=\"dLabel\"><datetimepicker ng-show=\"cluster.edit\" data-ng-model=\"cluster.date\" data-datetimepicker-config=\"{ dropdownSelector: '.my-toggle-select' }\"></datetimepicker></ul></div></div><div><h4>Cluster's TLE</h4></div><div class=\"control-group\" ng-class=\"{ 'has-error': form.tle_l1.$invalid }\"><label class=\"control-label\" for=\"tle_l1\">First line</label><input type=\"text\" name=\"tle_l1\" class=\"form-control\" style=\"width: 100%\" ng-model=\"cluster.tle_l1\" ng-pattern=\"/^[a-zA-Z0-9.\\s-]{69}$/\" ng-disabled=\"!cluster.edit\" required></div><div class=\"control-group\" ng-class=\"{ 'has-error': form.tle_l2.$invalid }\"><label class=\"control-label\" for=\"tle_l2\">Second line</label><input type=\"text\" name=\"tle_l2\" class=\"form-control\" style=\"width: 100%\" ng-model=\"cluster.tle_l2\" ng-pattern=\"/^[a-zA-Z0-9.\\s-]{69}$/\" ng-disabled=\"!cluster.edit\" required></div><hr><div style=\"display: table-row\" ng-hide=\"cluster.edit\"><div style=\"display: table-cell\"><a class=\"green-link link action-link\" ng-click=\"editCluster()\">(edit)</a></div></div><div style=\"display: table-row\" ng-show=\"cluster.edit\"><div style=\"display: table-cell; width: 50%\"><a class=\"green-link link action-link\" ng-click=\"saveCluster()\">(save)</a></div><div style=\"display: table-cell; width: 50%\"><a class=\"red-link link action-link\" ng-click=\"cancelCluster()\">(cancel)</a></div></div></div><div style=\"display: table-cell; width: 20px\"></div><div style=\"display: table-cell; width: 60%\"><div class=\"bottom-border\"><div style=\"display: table-cell\"><h4>UFO Objects</h4></div><div ng-hide=\"cluster.no_ufos\"><p class=\"no-items\">(no ufos)</p></div><span class=\"link ufo-item\" ng-click=\"editingUfo(value.object_id)\" ng-repeat=\"(index, value) in cluster.ufos\">Object #{{value.object_id}}<br ng-show=\"(index+1)%3==0\"></span><hr><div style=\"display: table-row\"><div style=\"display: table-cell; font-size: 75%\"><a class=\"green-link\" ng-show=\"cluster.no_ufos < cluster.max_objects\" ng-click=\"add()\">(+ add)</a> <a class=\"red-link\" ng-hide=\"(cluster.no_ufos < cluster.max_objects)\">MAXIMUM</a></div><div ng-show=\"cluster.no_ufos > 0\"><a class=\"red-link action-link\" ng-click=\"remove()\">(- del)</a></div></div></div><div class=\"bottom-border\"><div ng-hide=\"cluster.no_editing\"><p class=\"no-items\">(none in edition)</p></div><ol class=\"unsalted-list\"><li class=\"ufo-item\" ng-repeat=\"(index, i) in cluster.editing\"><div style=\"display: table-row\"><div style=\"display: table-cell; width: 50%; vertical-align: middle\"><h5>Object #{{ i.object_id }}</h5></div><div class=\"control-group\" style=\"column-span: all; vertical-align: middle\" ng-class=\"{ 'has-error': form.i_callsign.$invalid }\"><label class=\"control-label\" for=\"i_callsign\">Callsign</label><input type=\"text\" name=\"i_callsign\" class=\"form-control\" style=\"width: 100%\" ng-disabled=\"!i.edit\" ng-model=\"i.callsign\" ng-pattern=\"/^[a-zA-Z0-9]{3,8}$/\" required></div></div><div style=\"display: table-row\"><div style=\"display: table-cell\"><div class=\"control-group\" ng-class=\"{ 'has-error': form.i_tle_l1.$invalid }\"><label class=\"control-label\" for=\"i_tle_l1\">First line</label><input type=\"text\" name=\"i_tle_l1\" class=\"form-control\" style=\"width: 100%\" ng-disabled=\"!i.edit\" ng-model=\"i.tle_l1\" ng-pattern=\"/^[a-zA-Z0-9.\\s-]{69}$/\" required></div></div><div style=\"display: table-cell\"><div class=\"control-group\" ng-class=\"{ 'has-error': form.i_tle_l2.$invalid }\"><label class=\"control-label\" for=\"i_tle_l2\">Second line</label><input type=\"text\" name=\"i_tle_l2\" class=\"form-control\" style=\"width: 100%\" ng-disabled=\"!i.edit\" ng-model=\"i.tle_l2\" ng-pattern=\"/^[a-zA-Z0-9.\\s-]{69}$/\" required></div></div></div><div style=\"display: table-row\"><div style=\"display: table-cell\"><a class=\"green-link link action-link\" ng-disabled=\"!i.edit\" ng-click=\"save(i.object_id)\">(save)</a></div><div style=\"display: table-cell\"><a class=\"red-link link action-link\" ng-disabled=\"!i.edit\" ng-click=\"cancel(i.object_id)\">(cancel)</a></div></div><hr></li></ol></div><div><div><h4>Identified</h4></div><div ng-hide=\"cluster.no_identified\"><p class=\"no-items\">(none identified)</p></div><ol class=\"unsalted-list\"><li class=\"ufo-item\" ng-repeat=\"(index, i) in cluster.identified\"><div style=\"display: table-row\"><div style=\"display: table-cell; width: 50px\"><a class=\"red-link link action-link\" ng-click=\"forget(i.object_id)\">(forget)</a></div><div style=\"display: table-cell; vertical-align: middle\"><h5 style=\"vertical-align: middle\"><p>Object #{{ i.object_id }} <span ng-click=\"editingIded(i.object_id)\" style=\"font-size: 75%\">(as {{ i.callsign }})</span></p></h5></div></div><hr></li></ol></div></div></div></form></div><div class=\"modal-footer\"><button class=\"btn btn-primary\" ng-click=\"hide()\">(hide)</button></div>"
  );


  $templateCache.put('templates/leop/manageGroundStations.html',
    "<div class=\"modal-header\"><h3 class=\"modal-title\">Manage Ground Stations</h3></div><div class=\"modal-body\" style=\"display: table-row\"><form name=\"form\"><div style=\"width: 300px; display: table-cell; text-align: center\"><h4>Available GS</h4><select multiple ng-model=\"gsIds.aItems\" ng-options=\"aid as aid.groundstation_id for aid in gsIds.leop_gs_available\" style=\"width: 95%\" class=\"leop-gs-duallist\"></select></div><div style=\"width: 10px; display: table-cell; margin-top: 50px\"><button id=\"a2u\" class=\"btn\" ng-disabled=\"!gsIds.aItems.length\" ng-click=\"selectGs()\">&gt;</button> <button id=\"u2a\" class=\"btn\" ng-disabled=\"!gsIds.uItems.length\" ng-click=\"unselectGs()\">&lt;</button></div><div style=\"width: 300px; display: table-cell; text-align: center\"><h4>Choosen GS</h4><select multiple ng-model=\"gsIds.uItems\" ng-options=\"uid as uid.groundstation_id for uid in gsIds.leop_gs_inuse\" style=\"width: 95%\"></select></div></form></div><div class=\"modal-footer\"><button class=\"btn btn-primary\" ng-click=\"ok()\"><!--ng-disabled=\"!gsIds.toAdd || !gsIds.toRemove\">-->(ok)</button> <button class=\"btn btn-warning\" ng-click=\"cancel()\">(cancel)</button></div>"
  );


  $templateCache.put('templates/messages/messages.html',
    "<input type=\"checkbox\" name=\"messages-toggle\" id=\"messages-toggle\"><div ng-controller=\"messagesCtrl\" class=\"messages-area\"><div class=\"messages-top-padding\"></div><div ng-hide=\"data.length\"><p class=\"no-items-red\">(no messages)</p></div><div class=\"messages-content\"><div class=\"message-row\" ng-repeat=\"m in data\"><div class=\"message-ts-cell\"><p>{{ m.timestamp | date:'yyyy-MM-dd HH:mm:ss Z'}}</p></div><div class=\"message-gs-cell\"><p>{{ m.gs_identifier }}</p></div><div class=\"message-data-cell\"><span>{{ m.message }}</span></div></div></div><div class=\"messages-title\"><label for=\"messages-toggle\"></label></div></div>"
  );


  $templateCache.put('templates/notifier/logNotifier.html',
    "<input type=\"checkbox\" name=\"n-area-toggle\" id=\"n-area-toggle\"><div ng-controller=\"logNotifierCtrl\" class=\"n-area\"><div class=\"n-area-title\"><label for=\"n-area-toggle\"></label></div><div class=\"n-area-content\"><ul class=\"n-area-list\"><li ng-repeat=\"e in eventLog\"><div class=\"n-area-info-row\"><div class=\"n-area-type-cell\"><p class=\"{{ e.type }}\">[@{{ e.timestamp }}]</p></div><div class=\"n-area-content-cell\"><span class=\"{{ e.type }}\">{{ e.msg }}</span></div></div></li></ul></div></div>"
  );


  $templateCache.put('templates/passes/myGanttTpl.html',
    "<div class=\"gantt unselectable\" ng-cloak gantt-scroll-manager gantt-element-width-listener=\"ganttElementWidth\"><gantt-side><gantt-side-background></gantt-side-background><gantt-side-content></gantt-side-content><div gantt-resizer=\"gantt.side.$element\" gantt-resizer-event-topic=\"side\" gantt-resizer-enabled=\"{{$parent.gantt.options.value('allowSideResizing')}}\" resizer-width=\"sideWidth\" class=\"gantt-resizer\"><div ng-show=\"$parent.gantt.options.value('allowSideResizing')\" class=\"gantt-resizer-display\"></div></div></gantt-side><gantt-scrollable-header><gantt-header><gantt-header-columns><div ng-repeat=\"header in gantt.columnsManager.visibleHeaders\"><div class=\"gantt-header-row\" ng-class=\"{'gantt-header-row-last': $last, 'gantt-header-row-first': $first}\"><gantt-column-header ng-repeat=\"column in header\"></gantt-column-header></div></div></gantt-header-columns></gantt-header></gantt-scrollable-header><gantt-scrollable><gantt-body><gantt-body-background><gantt-row-background ng-repeat=\"row in gantt.rowsManager.visibleRows track by row.model.id\"></gantt-row-background></gantt-body-background><gantt-body-foreground><div class=\"gantt-current-date-line\" ng-show=\"currentDate === 'line' && gantt.currentDateManager.position >= 0 && gantt.currentDateManager.position <= gantt.width\" ng-style=\"{'left': gantt.currentDateManager.position + 'px' }\"></div></gantt-body-foreground><gantt-body-columns><gantt-column ng-repeat=\"column in gantt.columnsManager.visibleColumns\"><gantt-time-frame ng-repeat=\"timeFrame in column.visibleTimeFrames\"></gantt-time-frame></gantt-column></gantt-body-columns><gantt-body-rows><gantt-timespan ng-repeat=\"timespan in gantt.timespansManager.timespans track by timespan.model.id\"></gantt-timespan><gantt-row ng-repeat=\"row in gantt.rowsManager.visibleRows track by row.model.id\"><gantt-task ng-repeat=\"task in row.visibleTasks track by task.model.id\"></gantt-task></gantt-row></gantt-body-rows></gantt-body></gantt-scrollable><!-- Plugins --><ng-transclude></ng-transclude><!--\n" +
    "    ******* Inline templates *******\n" +
    "    You can specify your own templates by either changing the default ones below or by\n" +
    "    adding an attribute template-url=\"<url to your template>\" on the specific element.\n" +
    "    --><!-- Body template --><script type=\"text/ng-template\" id=\"template/ganttBody.tmpl.html\"><div ng-transclude class=\"gantt-body\" ng-style=\"{'width': gantt.width +'px'}\"></div></script><!-- Header template --><script type=\"text/ng-template\" id=\"template/ganttHeader.tmpl.html\"><div ng-transclude class=\"gantt-header\"\n" +
    "             ng-show=\"gantt.columnsManager.columns.length > 0 && gantt.columnsManager.headers.length > 0\"></div></script><!-- Side template --><script type=\"text/ng-template\" id=\"template/ganttSide.tmpl.html\"><div ng-transclude class=\"gantt-side\"></div></script><!-- Side content template--><script type=\"text/ng-template\" id=\"template/ganttSideContent.tmpl.html\"><div class=\"gantt-side-content\">\n" +
    "        </div></script><!-- Header columns template --><script type=\"text/ng-template\" id=\"template/ganttHeaderColumns.tmpl.html\"><div ng-transclude class=\"gantt-header-columns\"\n" +
    "              gantt-horizontal-scroll-receiver></div></script><script type=\"text/ng-template\" id=\"template/ganttColumnHeader.tmpl.html\"><div class=\"gantt-column-header\" ng-class=\"{'gantt-column-header-last': $last, 'gantt-column-header-first': $first}\">{{::column.label}}</div></script><!-- Body background template --><script type=\"text/ng-template\" id=\"template/ganttBodyBackground.tmpl.html\"><div ng-transclude class=\"gantt-body-background\"></div></script><!-- Body foreground template --><script type=\"text/ng-template\" id=\"template/ganttBodyForeground.tmpl.html\"><div ng-transclude class=\"gantt-body-foreground\"></div></script><!-- Body columns template --><script type=\"text/ng-template\" id=\"template/ganttBodyColumns.tmpl.html\"><div ng-transclude class=\"gantt-body-columns\"></div></script><script type=\"text/ng-template\" id=\"template/ganttColumn.tmpl.html\"><div ng-transclude class=\"gantt-column gantt-foreground-col\" ng-class=\"{'gantt-column-last': $last, 'gantt-column-first': $first}\"></div></script><script type=\"text/ng-template\" id=\"template/ganttTimeFrame.tmpl.html\"><div class=\"gantt-timeframe\"></div></script><!-- Scrollable template --><script type=\"text/ng-template\" id=\"template/ganttScrollable.tmpl.html\"><div ng-transclude class=\"gantt-scrollable\" gantt-scroll-sender ng-style=\"getScrollableCss()\"></div></script><script type=\"text/ng-template\" id=\"template/ganttScrollableHeader.tmpl.html\"><div ng-transclude class=\"gantt-scrollable-header\" ng-style=\"getScrollableHeaderCss()\"></div></script><!-- Rows template --><script type=\"text/ng-template\" id=\"template/ganttBodyRows.tmpl.html\"><div ng-transclude class=\"gantt-body-rows\"></div></script><!-- Timespan template --><script type=\"text/ng-template\" id=\"template/ganttTimespan.tmpl.html\"><div class=\"gantt-timespan\" ng-class=\"timespan.classes\">\n" +
    "        </div></script><!-- Task template --><script type=\"text/ng-template\" id=\"template/ganttTask.tmpl.html\"><div class=\"gantt-task\" ng-class=\"task.model.classes\">\n" +
    "            <gantt-task-background></gantt-task-background>\n" +
    "            <gantt-task-content></gantt-task-content>\n" +
    "            <gantt-task-foreground></gantt-task-foreground>\n" +
    "        </div></script><script type=\"text/ng-template\" id=\"template/ganttTaskBackground.tmpl.html\"><div class=\"gantt-task-background\" ng-style=\"{'background-color': task.model.color}\"></div></script><script type=\"text/ng-template\" id=\"template/ganttTaskForeground.tmpl.html\"><div class=\"gantt-task-foreground\">\n" +
    "            <div ng-if=\"task.truncatedRight\" class=\"gantt-task-truncated-right\">&gt;</div>\n" +
    "            <div ng-if=\"task.truncatedLeft\" class=\"gantt-task-truncated-left\">&lt;</div>\n" +
    "        </div></script><!-- Task content template --><script type=\"text/ng-template\" id=\"template/ganttTaskContent.tmpl.html\"><div class=\"gantt-task-content\"><span>{{task.model.name}}</span></div></script><!-- Row background template --><script type=\"text/ng-template\" id=\"template/ganttRowBackground.tmpl.html\"><div class=\"gantt-row gantt-row-height\"\n" +
    "             ng-class=\"row.model.classes\"\n" +
    "             ng-style=\"{'height': row.model.height}\">\n" +
    "            <div class=\"gantt-row-background\"\n" +
    "                 ng-style=\"{'background-color': row.model.color}\">\n" +
    "            </div>\n" +
    "        </div></script><!-- Row template --><script type=\"text/ng-template\" id=\"template/ganttRow.tmpl.html\"><div class=\"gantt-row gantt-row-height\"\n" +
    "             ng-class=\"row.model.classes\"\n" +
    "             ng-style=\"{'height': row.model.height}\">\n" +
    "            <div ng-transclude class=\"gantt-row-content\"></div>\n" +
    "        </div></script><!-- Side background template --><script type=\"text/ng-template\" id=\"template/ganttSideBackground.tmpl.html\"><div class=\"gantt-side-background\">\n" +
    "            <div class=\"gantt-side-background-header\">\n" +
    "                <div ng-show=\"gantt.columnsManager.columns.length > 0 && gantt.columnsManager.headers.length > 0\">\n" +
    "                    <div ng-repeat=\"header in gantt.columnsManager.headers\">\n" +
    "                        <div class=\"gantt-row-height\" ng-class=\"{'gantt-labels-header-row': $last, 'gantt-labels-header-row-last': $last}\"></div>\n" +
    "                    </div>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "            <div class=\"gantt-side-background-body\" ng-style=\"getMaxHeightCss()\">\n" +
    "                <div gantt-vertical-scroll-receiver>\n" +
    "                    <div class=\"gantt-row gantt-row-height \"\n" +
    "                         ng-class=\"row.model.classes\"\n" +
    "                         ng-repeat=\"row in gantt.rowsManager.visibleRows track by row.model.id\"\n" +
    "                         ng-style=\"{'height': row.model.height}\">\n" +
    "                        <div gantt-row-label class=\"gantt-row-label gantt-row-background\"\n" +
    "                             ng-style=\"{'background-color': row.model.color}\">\n" +
    "                        </div>\n" +
    "                    </div>\n" +
    "                </div>\n" +
    "            </div>\n" +
    "        </div></script></div>"
  );


  $templateCache.put('templates/passes/passes.html',
    "<input type=\"checkbox\" name=\"passes-toggle\" id=\"passes-toggle\"><div ng-controller=\"passSlotsCtrl\" class=\"passes-area\"><div class=\"passes-title\"><label for=\"passes-toggle\"></label></div><div ng-hide=\"data.length\"><p class=\"no-items-red\">(no passes)</p></div><div ng-show=\"data.length\" gantt class=\"passes-content\" data=\"data\" allow-side-resizing=\"false\" auto-expand=\"both\" template-url=\"templates/passes/myGanttTpl.html\"><gantt-labels></gantt-labels><gantt-movable></gantt-movable><gantt-tooltips></gantt-tooltips></div><div style=\"height: 25px\"></div></div>"
  );

}]);
