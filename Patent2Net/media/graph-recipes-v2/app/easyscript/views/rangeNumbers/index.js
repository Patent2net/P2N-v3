const InputView = require("../../../easyscript/controllers/input");

module.exports = (function(angular) {

    angular.component('easyRangeNumbers', {
        templateUrl: './components/easyScript/rangeNumbers/index.html',
        bindings: {
            rangeNumbers: '<'
        },
        controller: function EasyController($scope) {
            
            $scope.minInputController = $scope.$ctrl.rangeNumbers.minInputController
            $scope.maxInputController = $scope.$ctrl.rangeNumbers.maxInputController
        }
    });


});