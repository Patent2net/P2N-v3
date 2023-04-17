module.exports = (function(angular) {

    angular.component('easyRangeNumbers', {
        templateUrl: `${window.settings.root}/easyScript/views/rangeNumbers/index.html`,
        bindings: {
            rangeNumbers: '<'
        }
    });


});