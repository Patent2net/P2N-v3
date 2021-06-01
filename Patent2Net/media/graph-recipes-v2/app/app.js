'use strict';

window.app = (settings) => {

  window.settings = settings || {}
  
  // Requiring module's CSS
  require('angular-material/angular-material.min.css');

  // Requiring angular-related modules that will spit things in the global scope
  require('angular');
  require('angular-animate');
  require('angular-aria');
  require('angular-material');
  require('angular-route');
  require('angularjs-color-picker')

  // Making some modules global for the custom scripts to consume
  var d3 = require('d3');
  window.d3 = d3;
  var numeric = require('numeric');
  window.numeric = numeric;

  // Requiring some graphology libraries we are going to make global for the user
  var graphology = require('graphology');

  graphology.library = require('graphology-library/browser');
  window.graphology = graphology;
  window.Graph = graphology;

  var randomLayout = graphology.library.layout.random;

  var forceAtlas2Layout = graphology.library.layoutForceAtlas2;
  window.layout = {
    random: randomLayout,
    forceAtlas2: forceAtlas2Layout
  };

  window.ForceAtlas2Layout = graphology.library.FA2Layout;

  window.louvain = graphology.library.communitiesLouvain;

  // Requiring sigma
  window.SigmaWebGLRenderer = require('sigma/renderers/webgl').default;

  // Requiring own modules
  require('./view_upload/upload.js');
  require('./view_board/board.js');
  require('./recipes/_recipes_list_.js');

  // Declare app level module which depends on views, and components
  const app = angular.module('graphrecipes', [
    'ngRoute',
    'ngMaterial',
    'color.picker',
    'graphrecipes.view_upload',
    'graphrecipes.view_board',
    'graphrecipes.recipes_list'
  ])
  
  app.config(['$routeProvider', function($routeProvider) {
    $routeProvider.otherwise({redirectTo: '/upload'});
  }])

  // Filters
  .filter('number', function() {
    return function(d) {
      return +d
    }
  })
  .filter('percent', function() {
    return function(d) {
      return Math.round(+d*100)+'%'
    }
  })

  // Service
  .factory('cache', function(){
    var ns = {}
    ns.recipes = {}
    return ns
  })


  // Directives
  .directive('jsEditor', function ($timeout, $interval, $http, cache) {
    return {
      restrict: 'A',
      scope: {
        file: '=',
        remind: '='
      },
      templateUrl: `${settings.root}/jsEditor.html`,
      link: function(scope, element, attrs, ctrl) {
        if (scope.remind) {
          $timeout(function(){
            // INITIALIZATION
            if(cache.recipes[scope.file]){
              document.querySelector('#js-editor').textContent = cache.recipes[scope.file]
            }
            initAceJS()
          })
        } else {
          $http.get(scope.file).then(function (data) {
            $timeout(function(){
              // INITIALIZATION
              if(data.data){
                document.querySelector('#js-editor').textContent = data.data
                cache.recipes[scope.file] = data.data
              }
              initAceJS()
            })
          })
        }
        scope.$on('$destroy', function(){
          if (window.editor) {
            window.editor.destroy()
          }
        })
        scope.codeKeyPress = function(e){
          if((e.which == 13 || e.which == 10) && (e.ctrlKey || e.shiftKey)){
            scope.$parent.executeScript()
          }
        }

        function initAceJS() {
          // Init Ace JS editor panel
          // Note: we keep editor in global scope to be able to edit settings from the console
          window.editor = ace.edit("js-editor");
          window.editor.setTheme("ace/theme/clouds");
          window.editor.setFontSize(14)
          window.editor.getSession().setMode("ace/mode/javascript");
          window.editor.on('change', function(){
            $timeout(function(){
              cache.recipes[scope.file] = window.editor.getValue()
              scope.$apply()
            })
          })
        }
      }
    }
  })

  require('./components/heroDetail/index.js')(app);
  require('./components/easyScript/value/index.js')(app);
  require('./components/easyScript/block/index.js')(app);
  require('./components/easyScript/preset/index.js')(app);
  require('./components/easyScript/colors/index.js')(app);
  require('./components/easyScript/index.js')(app);
    
}
