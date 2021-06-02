module.exports = (function(angular) {

    angular.component('easyRangeNumbers', {
        templateUrl: './easyscript/views/rangeNumbers/index.html',
        bindings: {
            rangeNumbers: '<'
        },
        controller: function EasyController($scope) {
            console.log($scope)
        }
    });


});