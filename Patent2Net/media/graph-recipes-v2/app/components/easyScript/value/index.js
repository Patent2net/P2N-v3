module.exports = (function(angular) {

    angular.component('easyValue', {
        templateUrl: './components/easyScript/value/index.html',
        bindings: {
            data: '='
        },
        controller: function EastValueController($scope) {
            console.log("VALUE")
            console.log($scope)
        }
    });


});