angular.module('idle').run(['$templateCache', function($templateCache) {
  'use strict';

  $templateCache.put('templates/idle/timedoutDialog.html',
    "<div class=\"modal-header\"><h3>You've Timed Out!</h3></div><div class=\"modal-body\"><p>User has been idle for too long, logging out...</p></div>"
  );


  $templateCache.put('templates/idle/warningDialog.html',
    "<div class=\"modal-header\"><h3>User has been inactive for too long, session is about to expire.</h3></div><div class=\"modal-body\" ng-idle-countdown=\"countdown\" ng-init=\"countdown=5\"><p>Logging out in <span class=\"label label-warning\">{{countdown}}</span> <span ng-pluralize=\"\" count=\"countdown\" when=\"{'one': 'second', 'other': 'seconds' }\"></span></p><progressbar max=\"5\" value=\"countdown\" animate=\"true\" class=\"progress-striped active\" type=\"warning\"></div>"
  );

}]);
