'use strict';

const Value = require('../easyscript/models/value')
const Method = require('../easyscript/models/method')
const Variable = require('../easyscript/models/variable')

var isNumeric = require('../utils.js').isNumeric;
const RangeNumbersController = require('../easyscript/controllers/rangeNumbers');
const SelectBlockController = require("../easyscript/controllers/selectBlock");
const ColorsController = require('../easyscript/controllers/colors');

//Load all easy recipes
const easy_recipes = {
  sigma: require('../easy_recipes/sigma.js')
}

angular.module('graphrecipes.view_board', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/board', {
    templateUrl: `${window.settings.root}/view_board/board.html`,
    controller: 'BoardCtrl'
  });
}])

.controller('BoardCtrl', ['$scope', '$timeout',  'store', '$location', 'recipesList', '$http'
  ,function(               $scope ,  $timeout ,   store ,  $location,   recipesList ,  $http) {

  var gexf = graphology.library.gexf;

  // Scope variables
  $scope.filename
  $scope.filetitle
  $scope.originalGraph
  $scope.nodesCount
  $scope.edgesCount
  $scope.recipes = recipesList
  $scope.recipe = undefined
  $scope.lcdStatus = 'choose-recipe'
  $scope.status = 'list' // list | edit | run | end
  $scope.settings = window.settings
  $scope.easyscript = false
  $scope.esc
  $scope.directRun

  // Scope functions
  $scope.refreshGraph = function () {
    window.g = $scope.originalGraph
    if (window.g) {
      var format = d3.format(',')

      $scope.nodesCount = format(g.order)
      $scope.edgesCount = format(g.size)

      $scope.description = g.multi ? 'Multi ' : 'Simple '
      $scope.description += g.type + ' graph'
    } else {
      $timeout(function(){
        $location.url('/upload')
      }, 0)
    }
  }

  $scope.downloadOutput = function () {
    var xml = gexf.write(g);

    var blob = new Blob([xml], {'type':'text/gexf+xml;charset=utf-8'});
    saveAs(blob, store.get('graphname') + " via Graph Recipes.gexf");
  }

  $scope.pickRecipe = function(r) {
    $scope.lcdStatus = 'edit-script'
    $scope.recipe = r
    $scope.status = 'edit'
    $scope.remindRecipe = false
    // If easyscript version exist
    if (r.easy_name) {
      //Show easyscript version
      $scope.easy_recipe = easy_recipes[r.easy_name]
      $scope.esc = $scope.easy_recipe.createController(window.g)
      $scope.easyscript = true
    } else {
      //Run default script
      $scope.easy_recipe = null
      $scope.esc = null
      $scope.easyscript = false
      $scope.directRun = true
      $scope.executeScript($scope.settings.root+'/recipes/'+r.file)
    }
  }

   $scope.backToRecipe = function() {
    $scope.lcdStatus = 'edit-script'
    $scope.status = 'edit'
    if ($scope.directRun) {
      $scope.directRun = false
      $scope.remindRecipe = false
    } else {
      $scope.remindRecipe = true
    }
    
  }

  $scope.closeRecipe = function() {
    $scope.recipe = undefined
    $scope.lcdStatus = 'choose-recipe'
    $scope.status = 'list'
  }

  $scope.executeScript = function(script = null) {
    $scope.lcdStatus = 'cooking'
    $scope.status = 'run'
    $timeout(function(){
      var codePromise = null
      document.querySelector('#playground').innerHTML = ''
      if (script) {
        codePromise = fetch($scope.settings.root+'/recipes/'+$scope.recipe.file).then(res => {
          return res.text().then(text => {
            return text
          })
        }).then(e => {
          return e
        })
      } else {
        codePromise = new Promise((resolve, reject) => {
          if (!window.editor) {
            resolve(null)
          } else {
            resolve(window.editor.getValue())
          }
        })
      }

      codePromise.then(code => {
        try {

          if ($scope.easyscript) {
            $scope.easy_recipe.use(window.g, $scope.esc)
          } else {
            eval(';(function(){'+code+'})();')
          }

          $scope.lcdStatus = 'service'
          $scope.status = 'end'

          // Stop after a while
          $timeout(function(){
            if ($scope.lcdStatus == 'service')
              $scope.lcdStatus = 'waiting'
          }, 10000)
        } catch(e) {
          $scope.lcdStatus = 'error'
          console.error('[Script error]', e)
          $timeout(function(){
            alert('Merde :(\nThere is an issue with this script:\n\n' + e)
            $scope.backToRecipe()
          })
        }
                
      })

    }, 4000)
  }

  $scope.toggleEasyscript = function() {
    console.log($scope.easyscript)
    $scope.easyscript = !$scope.easyscript
  }

  $scope.completeCode = function() {
    
  }

  $scope.backToUpload = function() {
    $timeout(function(){
      $location.url('/upload')
    }, 0)
  }

  // Init
  $scope.filename = store.get('graphname')
  if (window.settings && window.settings.files) {
    const file = window.settings.files.find((file) => file.path.replace(/\.[^\.]*$/, '') == $scope.filename)
    if (file) $scope.filetitle = file.name
  }

  $scope.originalGraph = store.get('graph')
  $scope.refreshGraph()

  // Processing

}]);