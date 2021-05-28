module.exports = (function(angular) {

    angular.component('heroDetail', {
        templateUrl: './components/heroDetail/index.html',
        bindings: {
            hero: '='
        }
    });


});