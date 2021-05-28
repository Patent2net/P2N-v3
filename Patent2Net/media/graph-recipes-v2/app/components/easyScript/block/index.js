module.exports = (function(angular) {

    angular.component('easyBlock', {
        templateUrl: './components/easyScript/block/index.html',
        bindings: {
            data: '=',
            showChildModal: '&'
        },
        controller: function EastBlockController($scope) {
            console.log(this)
            console.log($scope)
        }
    });


});