module.exports = (function(angular) {

    angular.component('easyRenderSigma', {
        templateUrl: `${window.settings.root}/easy_recipes_view/sigma/index.html`,
        bindings: {
            esc: '<'
        }
    });

});