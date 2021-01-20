'use strict';

// Requiring module's CSS
require('angular-material/angular-material.min.css');

// Requiring angular-related modules that will spit things in the global scope
require('angular');
require('angular-animate');
require('angular-aria');
require('angular-material');
require('angular-route');

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
angular.module('graphrecipes', [
  'ngRoute',
  'ngMaterial',
  'graphrecipes.view_upload',
  'graphrecipes.view_board',
  'graphrecipes.recipes_list'
]).
config(['$routeProvider', function($routeProvider) {
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
    templateUrl: 'jsEditor.html',
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

.directive('lcd', function ($timeout, $interval) {
  return {
    restrict: 'A',
    scope: {
      animStatus: '='
    },
    templateUrl: 'lcd.html',
    link: function(scope, element, attrs, ctrl) {
      var obj = element.find('object')
      var sprites = [
        "wait",
        "smokesmall",
        "smokebig",
        "splash",
        "casserole",
        "flyingfoodbit",
        "cookoven",
        "cooktop1",
        "cooktop2",
        "cooklegs",
        "cookarmknife1",
        "cookarmknife2",
        "cookarmknife3",
        "foodcut",
        "foodbits",
        "foodstackbottom",
        "foodstackmiddle",
        "foodstacktop",
        "cooksleeping",
        "zzz",
        "ovenfood",
        "closedovendoor",
        "openovendoor",
        "closeddoor",
        "opendoor",
        "cookstanding",
        "cookarmnote",
        "pen3",
        "pen2",
        "pen1",
        "cookserving",
        "cookbubble",
        "clientbubble",
        "menu",
        "spoon",
        "dish",
        "clientarm1",
        "clientarm2",
        "flyingdishpiece1",
        "flyingdishpiece2",
        "clienthead1",
        "clienthead2",
        "clienthead3",
        "thinkbubble",
        "background"
      ]
      var animIntervals = []

      // obj.removeClass("ng-hide");

      $timeout(function(){
        // sprites.forEach(hideSprite)
        scope.$watch('animStatus', applyStatus)
      }, 100)

      function hideSprite(s) {
        if (obj[0].contentDocument)
          obj[0].contentDocument.getElementById(s).style.display = "none"
      }

      function showSprite(s) {
        if (obj[0].contentDocument)
          obj[0].contentDocument.getElementById(s).style.display = "inline"
      }

      function applyStatus(e, os, ns) {
        if (os != ns) {
          animIntervals.forEach(function(promise){
            $interval.cancel(promise)
          })
          sprites.forEach(hideSprite)
          switch (scope.animStatus) {
            case 'off':
              // Nothing to do, everything off by default
              break;

            case 'error':
              sprites
                .filter(function(){return Math.random()>0.5})
                .forEach(function(sprite){
                  showSprite(sprite)
                })
              break;

            case 'waiting':
              showSprite('background')
              showSprite('closeddoor')
              showSprite('openovendoor')
              showSprite('cooksleeping')
              showSprite('clienthead3')
              break;

            case 'choose-recipe':
              showSprite('background')
              showSprite('foodstacktop')
              showSprite('foodstackmiddle')
              showSprite('foodstackbottom')
              showSprite('closeddoor')
              showSprite('closedovendoor')
              showSprite('cooksleeping')
              addAnimInterval([
                {'zzz': true}, {'zzz': false}
              ], 600)
              addAnimInterval([
                {'clienthead3': true , 'thinkbubble': true , 'clienthead1': false, 'clientarm1': false, 'menu': false},
                {'clienthead3': false, 'thinkbubble': false, 'clienthead1': true , 'clientarm1': true , 'menu': true}
              ], 1500)
              break;

            case 'edit-script':
              showSprite('background')
              showSprite('foodstacktop')
              showSprite('foodstackmiddle')
              showSprite('foodstackbottom')
              showSprite('opendoor')
              showSprite('closedovendoor')
              showSprite('clientarm1')
              showSprite('cookstanding')
              showSprite('menu')
              addAnimInterval([
                {
                  'clienthead1': false,
                  'clienthead2': true,
                  'clientbubble': true,
                  'cookbubble': false
                },
                {
                  'clienthead1': true,
                  'clienthead2': false,
                  'clientbubble': false,
                  'cookbubble': true
                }
              ], 9*75)
              addAnimInterval([
                {'cookarmnote': true, 'pen1': true},
                {'pen1': false, 'pen2': true},
                {'pen2': false, 'pen3': true},
                {'pen3': false, 'pen2': true},
                {'pen2': false, 'pen1': true},
                {'pen1': false, 'pen2': true},
                {'pen2': false, 'pen3': true},
                {'pen3': false, 'pen2': true},
                {'pen2': false, 'pen1': true},
                {'pen1': false, 'cookarmnote': false},
                {},
                {},
                {},
                {},
                {},
                {},
                {},
                {}
              ], 75)
              break;

            case 'cooking':
              showSprite('background')
              showSprite('closeddoor')
              showSprite('closedovendoor')
              showSprite('clienthead3')
              showSprite('casserole')
              addAnimInterval([
                {
                  'foodcut': true,
                  'cooklegs': true,
                  'splash': false,
                  'cooktop1': false,
                  'cooktop2': true,
                  'cookarmknife1': true
                },
                {'cookarmknife1': false, 'cookarmknife2': true},
                {'cookarmknife2': false, 'cookarmknife3': true, 'foodbits': true},
                {'cookarmknife3': false, 'cookarmknife2': true},
                {'cookarmknife2': false, 'cookarmknife1': true, 'foodbits': false},
                {'cookarmknife1': false, 'cookarmknife2': true},
                {'cookarmknife2': false, 'cookarmknife3': true, 'foodbits': true},
                {'cookarmknife3': false, 'cookarmknife2': true},
                {'cookarmknife2': false, 'cookarmknife1': true, 'foodbits': false},
                {'cookarmknife1': false, 'cookarmknife2': true},
                {'cookarmknife2': false, 'cookarmknife3': true, 'foodbits': true},
                {
                  'cookarmknife3': false,
                  'foodbits': false,
                  'foodcut': false,
                  'cooktop2': false,
                  'cooktop1': true,
                },
                {'flyingfoodbit': true},
                {
                  'flyingfoodbit': false,
                  'splash': true
                }
              ], 50)

              addAnimInterval([
                {
                  'foodstackbottom': true,
                  'foodstackmiddle': true
                },
                {'foodstackmiddle': false},
                {'foodstackbottom': false}
              ], 14*50)

              // Phase 2
              $timeout(function(){
                if (scope.animStatus != 'cooking') { return }
                animIntervals.forEach(function(promise){
                  $interval.cancel(promise)
                })
                sprites.forEach(hideSprite)
                showSprite('background')
                showSprite('clienthead3')
                showSprite('closeddoor')
                addAnimInterval([
                  {
                    'cookoven': true,
                    'openovendoor': true,
                    'casserole': true
                  },
                  {'casserole': false, 'ovenfood': true},
                  {'openovendoor': false, 'closedovendoor': true}
                ], 150)

                // Phase 3
                $timeout(function(){
                  if (scope.animStatus != 'cooking') { return }
                  animIntervals.forEach(function(promise){
                    $interval.cancel(promise)
                  })
                  sprites.forEach(hideSprite)
                  showSprite('background')
                  showSprite('clienthead3')
                  showSprite('closeddoor')
                  showSprite('closedovendoor')
                  showSprite('ovenfood')
                  showSprite('cooksleeping')
                  showSprite('wait')
                  addAnimInterval([
                    {'zzz': true}, {'zzz': false}
                  ], 600)
                  addAnimInterval([
                    {'smokebig': true, 'smokesmall': false}, {'smokebig': false, 'smokesmall': true}
                  ], 800)

                }, 3*150)

              }, 14*50*3)

              break;

            case 'service':
              showSprite('background')
              showSprite('closeddoor')
              showSprite('clienthead3')
              addAnimInterval([
                {
                  'closedovendoor': true,
                  'cookoven': true,
                  'ovenfood': true
                },
                {'closedovendoor': false, 'openovendoor': true},
                {
                  'ovenfood': false,
                  'cookoven': false,
                  'closeddoor': false,
                  'opendoor': true,
                  'cookserving': true,
                },
                {'clienthead3': false, 'clienthead2': true},
                {'cookserving': false, 'cookstanding': true, 'dish': true},
                {
                  'clienthead2': false,
                  'clienthead1': true,
                  'clientarm1': true,
                  'spoon': true,
                  'cookstanding': false,
                  'opendoor': false,
                  'closeddoor': true,
                  'cooksleeping': true
                }
              ], 300)

              // Phase 2
              $timeout(function(){
                if (scope.animStatus != 'service') { return }
                animIntervals.forEach(function(promise){
                  $interval.cancel(promise)
                })
                sprites.forEach(hideSprite)
                showSprite('background')
                showSprite('closeddoor')
                showSprite('openovendoor')
                showSprite('cooksleeping')
                showSprite('dish')
                addAnimInterval([
                  {'zzz': true}, {'zzz': false}
                ], 600)
                addAnimInterval([
                  {
                    'clienthead1': false,
                    'clienthead2': true,
                    'clientarm1': true,
                    'spoon': true
                  },
                  {
                    'clientarm1': false,
                    'spoon': false,
                    'clientarm2': true
                  },
                  {'flyingdishpiece1': true},
                  {'flyingdishpiece1': false, 'flyingdishpiece2': true, 'clientarm2': false, 'clientarm1': true},
                  {'clienthead2': false, 'clienthead1': true, 'flyingdishpiece2': false, 'spoon': true}
                ], 100)
              }, 6*300)
          }
        }
      }

      function addAnimInterval(sequence, delay) {
        var sprite
        for(sprite in sequence[0]) {
          if (sequence[0][sprite]) {
            showSprite(sprite)
          } else {
            hideSprite(sprite)
          }
        }

        var count = 0
        var interval = $interval(function(){
          count = count + 1
          var moment = sequence[count%sequence.length]
          for(sprite in moment) {
            if (moment[sprite]) {
              showSprite(sprite)
            } else {
              hideSprite(sprite)
            }
          }
        }, delay || 500)
        animIntervals.push(interval)
      }
    }
  }
})
