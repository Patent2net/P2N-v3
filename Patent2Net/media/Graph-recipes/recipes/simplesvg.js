var settings = {}

// Feel free to edit following settings

// General
settings.save_at_the_end = false
settings.width = 1000
settings.height = 1000
settings.offset = 20 // Margin

// Nodes
settings.node_size = 0.4

// Nodes labels
settings.label_white_border_thickness = 3.0
settings.label_font_size = 12
settings.label_font_family = 'Open Sans Condensed, sans-serif'

// Edges
settings.edge_thickness = 1.0

// --- (end of settings)

// Create the svg space
var svgContainer = d3.select("#playground").append('div')
	.attr('style', 'width: '+settings.width+'px; height:'+settings.height+'px')
var svg = svgContainer.append("svg")
	.attr('width', settings.width)
	.attr('height', settings.height)

// Fix missing coordinates and/or colors
addMissingVisualizationData()

// Change the coordinates of the network to fit the SVG space
rescaleGraphToGraphicSpace()

// Set a default color to each node (in case they have no "color" attribute)
g.nodes().forEach(function(nid){
	var n = g.getNodeAttributes(nid)
	if (n.color === undefined){
		n.color = 'rgb(200,200,200)'
	}
})

// Draw edges
g.edges().forEach(function(eid){
	var e = g.getEdgeAttributes(eid)
	var ns = g.getNodeAttributes(g.source(eid))
	var nt = g.getNodeAttributes(g.target(eid))

	// Set edge width
	var edgeWidth = (e.weight || 1) * settings.edge_thickness
	
	// White background
	drawEdge({
		source: ns
	, target: nt
	, width: edgeWidth
	, style: {
			fill: '#FFF'
		, stroke: '#FFF'
		, 'stroke-width': settings.edge_stroke_width
		}
	})

	// Actual edge
	drawEdge({
		source: ns
	, target: nt
	, width: edgeWidth
	, style: {
			fill: '#DDD'
		, stroke: '#DDD'
		, 'stroke-width': settings.edge_stroke_width
		}
	})
	
})

// Draw the nodes
g.nodes().forEach(function(nid){
	var n = g.getNodeAttributes(nid)

	var color = d3.rgb(n.color)
	
	var circle = d3.path()
	circle.arc(
		n.x
	,	n.y
	,	settings.node_size * n.size
	, 0
	, Math.PI * 2
	)

	svg.append("path")
		.attr('d', circle.toString())
		.attr('fill', color.toString())

})

// Draw labels
g.nodes().forEach(function(nid){
	var n = g.getNodeAttributes(nid)

	var color = d3.rgb(n.color)

	var labelCoordinates = {
		x: n.x + settings.node_size * n.size * 1.2,
		y: n.y + 0.32 * settings.label_font_size
	}

	// Label's White border
	svg.append('text')
		.attr('x', labelCoordinates.x)
		.attr('y', labelCoordinates.y)
		.text(n.label)
		.attr('font-family', settings.label_font_family)
		.attr('text-anchor', 'start')
		.attr('font-size', settings.label_font_size)
		.attr('stroke-width', settings.label_white_border_thickness)
		.attr('stroke', '#FFFFFF')
		.attr('fill', 'none')

	// Label itself
	svg.append('text')
		.attr('x', labelCoordinates.x)
		.attr('y', labelCoordinates.y)
		.text(n.label)
		.attr('font-family', settings.label_font_family)
		.attr('text-anchor', 'start')
		.attr('font-size', settings.label_font_size)
		.attr('fill', color)
	
})

// Save if needed
if (settings.save_at_the_end) {
	saveSVG()
}

// ---
// Functions

function saveSVG() {
	// Download SVG
	var svgFileContent = []
	svgFileContent.push('<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="'+settings.width+'" height="'+settings.height+'" viewBox="0 0 '+settings.width+' '+settings.height+'">')
	svgFileContent.push(svg.html())
	svgFileContent.push('</svg>')

	var blob = new Blob(svgFileContent, {type: "image/svg+xml;charset=utf-8"})
	saveAs(blob, store.get('graphname') + ".svg")
}

function drawEdge(s /*settings*/){

	if (
			s.source === undefined
	||	s.target === undefined
	) {
		console.error('Cannot draw edge without a source and target', s)
	}

	s.width = s.width || 1

	s.style = s.style || {fill:'#EEE', stroke:'#EEE', 'stroke-width': settings.edge_thickness}

	// Draw edge

	var edgePath = d3.path()
	edgePath.moveTo(s.source.x,	s.source.y)
	edgePath.lineTo(s.target.x,	s.target.y)

	var edgePathElement = svg.append("path")
		.attr('d', edgePath.toString())
	
	var k
	for (k in s.style) {
		edgePathElement.attr(k, s.style[k])
	}
}

function rescaleGraphToGraphicSpace() {

  // General barycenter resize
  var xbarycenter = 0
  var ybarycenter = 0
  var wtotal = 0
  var dx
  var dy
  var ratio

  g.nodes().forEach(function(nid){
  	var n = g.getNodeAttributes(nid)
    // We use node size as weight (default to 1)
    n.size = n.size || 1
    xbarycenter += n.size * n.x
    ybarycenter += n.size * n.y
    wtotal += n.size
  })
  xbarycenter /= wtotal
  ybarycenter /= wtotal

  var dmax = 0 // Maximal distance from barycenter
  g.nodes().forEach(function(nid){
  	var n = g.getNodeAttributes(nid)
    var d = Math.sqrt( Math.pow(n.x - xbarycenter, 2) + Math.pow(n.y - xbarycenter, 2) )
    dmax = Math.max(dmax, d)
  })

  ratio = ( Math.min(settings.width, settings.height) - 2 * settings.offset ) / (2 * dmax)

  g.nodes().forEach(function(nid){
  	var n = g.getNodeAttributes(nid)
    n.x = settings.width / 2 + (n.x - xbarycenter) * ratio
    n.y = settings.height / 2 + (n.y - ybarycenter) * ratio
    n.size *= ratio
  })

}

function addMissingVisualizationData() {
  var colorIssues = 0
  var coordinateIssues = 0
  g.nodes().forEach(function(nid){
    var n = g.getNodeAttributes(nid)
    if (!isNumeric(n.x) || !isNumeric(n.y)) {
      var c = getRandomCoordinates()
      n.x = c[0]
      n.y = c[1]
      coordinateIssues++
    }
    if (!isNumeric(n.size)) {
      n.size = 1
    }
    if (n.color == undefined) {
      n.color = '#665'
      colorIssues++
    }
  })

  if (coordinateIssues > 0) {
    alert('Note: '+coordinateIssues+' nodes had coordinate issues. We carelessly fixed them.')
  }

  function isNumeric(n) {
    return !isNaN(parseFloat(n)) && isFinite(n)
  }
  
  function getRandomCoordinates() {
    var candidates
    var d2 = Infinity
    while (d2 > 1) {
      candidates = [2 * Math.random() - 1, 2 * Math.random() - 1]
      d2 = candidates[0] * candidates[0] + candidates[1] * candidates[1]
    }
    var heuristicRatio = 5 * Math.sqrt(g.order)
    return candidates.map(function(d){return d * heuristicRatio})
  }
}