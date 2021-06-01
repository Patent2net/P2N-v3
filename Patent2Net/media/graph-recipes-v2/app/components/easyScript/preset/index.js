module.exports = (function(angular) {

    angular.component('easyPreset', {
        templateUrl: './components/easyScript/preset/index.html',
        bindings: {
            data: '<',
            callback: '<'
        },
        controller: function EastValueController($scope) {
            console.log("PRESET")
            console.log($scope)
        }
    });


});