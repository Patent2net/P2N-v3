module.exports = (function(angular) {

    angular.component('easyInput', {
        templateUrl: './components/easyScriptv2/input/index.html',
        bindings: {
            input: '<'
        },
        controller: function EasyController($scope) {
            $scope.value = $scope.$ctrl.input.getValue()
            $scope.type = $scope.$ctrl.input.getReturnType()

            $scope.$watch('value', function(newValue) {
                let value = Math.floor(newValue) || newValue

                $scope.$ctrl.input.setValue(value)
            })
        }
    });


});