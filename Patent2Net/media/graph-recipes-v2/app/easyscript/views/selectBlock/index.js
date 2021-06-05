const Value = require("../../models/value");

module.exports = (function(angular) {

    angular.component('easySelectBlock', {
        templateUrl: `${window.settings.root}/easyScript/views/selectBlock/index.html`,
        bindings: {
            selectBlock: '<'
        },
        controller: function EastBlockController($scope, $timeout) {
            $scope.dropdown = false
            $scope.dropdownshow = false


            $timeout(function() {
                console.log($scope.$ctrl.selectBlock)
            })

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
        }
    });


});