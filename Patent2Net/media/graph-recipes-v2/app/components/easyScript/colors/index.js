module.exports = (function(angular) {

    angular.component('easyColors', {
        templateUrl: './components/easyScript/colors/index.html',
        bindings: {
            data: '<',
            callback: '<'
        },
        controller: function EastValueController($scope) {
            console.log("COLORS")
            console.log($scope.$ctrl)
            console.log($scope.$ctrl.data)
            
            $scope.options = {
                format: ['hex'],
                alpha: false,
                dynamicHue: false,
            };
        }
    });


});