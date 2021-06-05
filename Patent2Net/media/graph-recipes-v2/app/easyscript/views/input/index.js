module.exports = (function(angular) {

    angular.component('easyInput', {
        templateUrl: `${window.settings.root}/easyScript/views/input/index.html`,
        bindings: {
            input: '<'
        }
    });
});