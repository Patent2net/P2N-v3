module.exports = (function(angular) {

    angular.component('easyBlock', {
        templateUrl: './easyscript/views/block/index.html',
        bindings: {
            block: '<'
        },
        controller: function EastValueController($scope) {
            console.log("PRESET")
            console.log($scope)
        }
    });


});