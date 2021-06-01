'use strict';

const Math = require('../easyscript/blocks/math')
const Value = require('../easyscript/blocks/value')
const Method = require('../easyscript/blocks/method')
const Variable = require('../easyscript/blocks/variable')

var isNumeric = require('../utils.js').isNumeric;

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

  const easyscriptdatacallback = (name) => {
    return function(newval){
      if (newval.type) {
        $scope.easyscriptdata[name]['default'] = newval;
      }
    }
  }

  $scope.sizesCallback = easyscriptdatacallback('sizes')
  $scope.colorsCallback = easyscriptdatacallback('colors')
  $scope.minSizeCallback = easyscriptdatacallback('min_size')
  $scope.maxSizeCallback = easyscriptdatacallback('max_size')


  const preAttribute = (name, type, value) => {
    return {
      name: name,
      type: type,
      new: () => {
        return new Method(
          'getNodeAttribute', 
          { 
            node: new Variable('node'),
            attribute: new Value(value) 
          },
          { 'preset': { name, type, value } }
        )

      }
    }
  }

  $scope.easyscriptdata = {
    'sizes': {
      'type': 'number',
      'default': new Value(20),
      'context': {
        variables: {
            'node': {
                type: 'object',
                name: 'node',
                title: 'Noeud'
            },
            'size': {
                type: 'number',
                name: 'size',
                title: 'Taille initial'
            }
        },
        methods: {
            'getNodeAttribute': {
                returnType: 'unknown',
                name: 'graph.getNodeAttribute',
                title: 'Récuperer l\'attribut d\'un noeud',
                params: [
                    {
                        type: 'object',
                        name: 'node',
                        title: 'Noeud'
                    },
                    {
                        type: 'text',
                        name: 'attribute',
                        tile: 'Nom de l\'attribut'
                    }
                ]
            }
        }
      },
      'presets': [
        preAttribute('Categorie', 'number', 'Category'),
        preAttribute('Nom du label', 'string' ,'Label2')
      ]
    },
    'colors': {
      'type': 'list',
      'default': new Value(["#00cccc", "#ff6633", "#119933"], { colors: { labels: ['first element', 'second element']}})
    },
    'min_size': {
      'type': 'number',
      'default': new Value(3),
      'context': {}
    },
    'max_size': {
      'type': 'number',
      'default': new Value(12),
      'context': {}
    }
  }
  
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
  }

   $scope.backToRecipe = function() {
    $scope.lcdStatus = 'edit-script'
    $scope.status = 'edit'
    $scope.remindRecipe = true
  }

  $scope.closeRecipe = function() {
    $scope.recipe = undefined
    $scope.lcdStatus = 'choose-recipe'
    $scope.status = 'list'
  }

  $scope.executeScript = function() {
    $scope.lcdStatus = 'cooking'
    $scope.status = 'run'
    $timeout(function(){
      document.querySelector('#playground').innerHTML = ''
      var code = window.editor.getValue()
      try {
        eval(';(function(){'+code+'})();')
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