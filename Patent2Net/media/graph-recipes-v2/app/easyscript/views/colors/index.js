module.exports = (function(angular) {

    angular.component('easyColors', {
        templateUrl: `${window.settings.root}/easyScript/views/colors/index.html`,
        bindings: {
            colors: '<'
        },
        controller: function EastValueController($scope) {
            console.log("COLORS")
            
            $scope.options = {
                format: 'hex',
                alpha: false,
                dynamicHue: false,
                case: 'upper'
            };
            
            $scope.$watch('$ctrl.data.value', function() {
                console.log("CHANGE")
            })

            $scope.eventApi = {
                onChange:  function(api, color, $event) {
                    console.log(api, color, $event)
                }
            }
        }
    });


});