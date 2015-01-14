/**
 * Created by rtubio on 1/13/15.
 */

angular.module('idle', ['ui.bootstrap']);

angular.module('idle')
    .controller('idleCtrl', [
        '$scope', '$modal',
        function ($scope, $modal) {
            'use strict';

            $scope.started = true;

            function closeModals() {
                if ($scope.warning) {
                    $scope.warning.close();
                    $scope.warning = null;
                }

                if ($scope.timedout) {
                    $scope.timedout.close();
                    $scope.timedout = null;
                }
            }

            $scope.$on('$idleStart', function () {
                closeModals();

                $scope.warning = $modal.open({
                    templateUrl: 'idle/warningDialog.html',
                    windowClass: 'modal-danger'
                });

            });

            $scope.$on('$idleEnd', function () {
                closeModals();
            });

            $scope.$on('$idleTimeout', function () {
                closeModals();
                $scope.timedout = $modal.open({
                    templateUrl: 'idle/timedoutDialog.html',
                    windowClass: 'modal-danger'
                });
            });

        }]);