const ColorsController = require("../easyscript/controllers/colors")
const RangeNumbersController = require("../easyscript/controllers/rangeNumbers")
const SelectBlockController = require("../easyscript/controllers/selectBlock")
const Method = require("../easyscript/models/method")
const Value = require("../easyscript/models/value")
const Variable = require("../easyscript/models/variable")

const createController = (g) => {

  console.log("SIGMA" + g)

  return {
    rangeSize: new RangeNumbersController(5, 10, { type: 'px' }),
    sizes: new SelectBlockController([
      {
        name: 'Valeur aléatoire',
        type: 'number',
        block: new Method(
          'random', 
          {}
        )
      },
      {
        name: 'Valeur par defaut',
        type: 'number',
        block: new Variable('size')
      },
      {
        name: 'Choisir une valeur',
        type: 'number',
        value: 10,
        onlyNumber: true
      },
    ]),
    colors: new ColorsController(["Oui", "Non"],["#00cccc", "#ff6633", "#119933"])
  }
}

const use = (g, controllers) => {

  // Parameters
  var DEFAULT_NODE_COLOR = '#808080';
  var DEFAULT_EDGE_COLOR = '#ccc';

  var rangeSize = controllers['rangeSize']

  var MIN_NODE_SIZE = rangeSize.minInputController.block.run();
  var MAX_NODE_SIZE = rangeSize.maxInputController.block.run();

  var FA2_SETTINGS = {
    barnesHutOptimize: g.order > 2000,
    strongGravityMode: true,
    gravity: 0.05,
    scalingRatio: 10,
    slowDown: 1 + Math.log(g.order)
  };

  var CATEGORY = "category";
  var COLORS = {
    e: '#c75a93',
    q: '#60a862'
  };


  var classesIndex = {}
  var cl
  g.nodes().forEach(function(nid){
    classesIndex[g.getNodeAttribute(nid, CATEGORY)] = true
  })
  var colors = ["#00cccc", "#ff6633", "#119933", "#cc0066","#091ba1","#ecd3cb","#0f1110", "#e066a3","#b0c39c","#5f93bc","#d27533","#b05edc","#67a43a","#da50a5","#599a75","#de4e55","#867bd3","#a3884c","#bc7590"]
  var count = 0
  for (cl in classesIndex) {
    if (count < colors.length) {
      classesIndex[cl] = colors[count]
    } else {
      classesIndex[cl] = '#AAA'
    }
    count++
  }


  // NOTE: use `true` if you don't want to "pollute" your graph with
  // visual attributes.
  var CLONE = true;
  //let classesIndex = new Set();
  // Cloning & decorating
  var graph = CLONE ? g.copy() : g;

  graph.nodes().forEach(function(node) {
  //  classesIndex .add(graph.getNodeAttribute(node, 'color'))
    // Color
    graph.updateNodeAttribute(node, 'color', function(color) {
      if (CATEGORY)
        return classesIndex[graph.getNodeAttribute(node, CATEGORY)] || DEFAULT_NODE_COLOR;

      return color || DEFAULT_NODE_COLOR;
    });

    // Size
    graph.updateNodeAttribute(node, 'size', function(size) {
      return controllers['sizes'].blockController.block.run({
        "random": {
          'method': Math.random,
          'params_id': []
        },
        "size": size,
        "node": node
      }) || graph.degree(node);
    });

    // Position
    function randomPositionIfNeeded(x) {
      return typeof x === 'number' ? x : Math.random();
    }

    graph.updateNodeAttribute(node, 'x', randomPositionIfNeeded);
    graph.updateNodeAttribute(node, 'y', randomPositionIfNeeded);
  });

  graph.edges().forEach(function(edge) {

    // Color
    graph.updateEdgeAttribute(edge, 'color', function(color) {
      return color || DEFAULT_EDGE_COLOR;
    });
  });

  // Scales
  var sizes = graph.nodes().map(function(node) {
    return graph.getNodeAttribute(node, 'size');
  });

  var nodeScale = d3.scaleLinear()
    .domain([Math.min.apply(null, sizes), Math.max.apply(null, sizes)])
    .range([MIN_NODE_SIZE, MAX_NODE_SIZE]);

  graph.nodes().forEach(function(node) {
    graph.updateNodeAttribute(node, 'size', nodeScale);
  });

  // Rendering
  var playground = document.getElementById('playground');
  playground.innerHTML = '<div id="container"></div>';
  playground.style.width = '100%';
  playground.style.height = '100%';
  playground.style.position = 'relative';

  var container = document.getElementById('container');
  container.style.width = '100%';
  container.style.height = '100%';
  container.style.position = 'absolute';

  var renderer = new SigmaWebGLRenderer(graph, container);
  var camera = renderer.getCamera();

  // Layout
  var layout = new ForceAtlas2Layout(graph, {settings: FA2_SETTINGS});

  // Padding
  document.querySelectorAll('#playground, #playground > #container, #playground > #container > canvas').forEach(function(dom) {
    dom.style.padding = '0px';
  });

  // Buttons
  var buttons = document.createElement('div');
  buttons.id = 'buttons';
  buttons.style.position = 'absolute';
  buttons.style.left = '0px';
  buttons.style.top = '0px';
  buttons.innerHTML = [
    '<button id="layout-button">Start Layout</button>',
    '<button id="rescale-button">Rescale</button>'
  ].join('');

  playground.appendChild(buttons);

  // Layout interaction
  var layoutButton = document.getElementById('layout-button');

  layoutButton.onclick = function() {
    if (layout.running) {
      layout.stop();
      layoutButton.innerText = 'Start Layout';
    }
    else {
      layout.start();
      layoutButton.innerText = 'Stop Layout';
    }
  };

  // Camera interaction
  var rescaleButton = document.getElementById('rescale-button');

  rescaleButton.onclick = function() {
    camera.animatedReset();
  };

  // Display legend
  var legend = d3.select('#playground').append('div')
    .style('width', '150px')
    .style('font-family', '"Raleway", sans-serif')
    .style('background-color', '#FFF')
    .style('margin', '12px')
    .style('border', '1px solid #AAA')
    .style('padding', '12px')
  legend.append('h3')
    .text('Legend')
    .style('margin-top', '0')
  legend.append('h4')
    .text('Color by ' + CATEGORY)
  for (cl in classesIndex) {
    var color = classesIndex [cl]
    var div = legend.append('div')
      .style('margin-bottom', '6px')
    div.append('div')
      .style('display', 'inline-flex')
      .style('width', '18px')
      .style('height', '18px')
      .style('border-radius', '9px')
      .style('background-color', color)
    div.append('div')
      .style('display', 'inline-flex')
      .style('padding-left', '6px')
      .style('vertical-align', 'top')
      .text(cl)
  }

}

module.exports = {
  use, 
  createController
}