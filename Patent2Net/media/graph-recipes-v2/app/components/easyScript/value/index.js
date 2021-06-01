module.exports = (function(angular) {

    angular.component('easyValue', {
        templateUrl: './components/easyScript/value/index.html',
        bindings: {
            data: '<',
            callback: '<'
        },
        controller: function EastValueController($scope) {
            console.log("VALUE")
            console.log($scope)

            $scope.dropdown = true

            $scope.showDropdown = function() {
                $scope.dropdown = true
            }

            $scope.hideDropdown = function() {
                $scope.modal = false
            }

            $scope.setValue = function() {
                const data = $scope.$ctrl.data
                data.value = Math.floor(data.value) || data.value

                $scope.$ctrl.callback(data)
            }

        }
    });


});