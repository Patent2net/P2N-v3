module.exports = (function(angular) {

    angular.component('easyScript', {
        templateUrl: './components/easyScript/index.html',
        bindings: {
            data: '='
        },
        controller: function EastScriptController($scope) {
            console.log(("Easyscript"))
            console.log($scope)

            $scope.modal = false
            $scope.showChildModal = function() {
                $scope.modal = true
            }

            $scope.hideChildModal = function() {
                $scope.modal = false
            }
        }
    });

});