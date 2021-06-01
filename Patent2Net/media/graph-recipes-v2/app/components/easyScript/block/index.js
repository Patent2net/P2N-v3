const Value = require("../../../easyscript/blocks/value");

module.exports = (function(angular) {

    angular.component('easyBlock', {
        templateUrl: './components/easyScript/block/index.html',
        bindings: {
            data: '<',
            showChildModal: '&',
            callback: '<',
            presets: '<'
        },
        controller: function EastBlockController($scope, $timeout) {
            console.log(this)
            console.log($scope)

            $scope.dropdown = false
            $scope.dropdownshow = false

            $scope.toggleDropdown = function() {
                $scope.dropdown = !$scope.dropdown
                $scope.dropdownshow = true

                if (!$scope.dropdown) {
                    $timeout(() => {
                        $timeout(function(){
                            $scope.dropdownshow = false
                        })
                    }, 100);
                }
            }

            $scope.usePreset = function(preset) {
                console.log(preset)
                $scope.$ctrl.callback(preset.new())
            }

            $scope.useValue = function() {
                $scope.$ctrl.callback(
                    new Value(0)
                )
            }
        }
    });


});