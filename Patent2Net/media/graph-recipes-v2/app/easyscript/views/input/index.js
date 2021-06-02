module.exports = (function(angular) {

    angular.component('easyInput', {
        templateUrl: './easyscript/views/input/index.html',
        bindings: {
            input: '<'
        },
        controller: function EasyController($scope, $timeout) {
            $scope.prevValue = null

            $timeout(function() {
                $scope.prevValue = $scope.$ctrl.input.block.value;
            })

            $scope.setValue = function(e) {
                $scope.$ctrl.input.onValueChange($scope.$ctrl.input.block.value, $scope.prevValue);
                $scope.prevValue = $scope.$ctrl.input.block.value;
            }
        }
    });
});