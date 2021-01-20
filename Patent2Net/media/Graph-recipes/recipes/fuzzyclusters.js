var settings = {}

// Feel free to edit following settings

// WHICH NODE ATTRIBUTE DESCRIBES CLUSTERS?
settings.cluster_attribute = 'IPCDiversity' // select between        ["category","size",Citations","Famille","NbBrevets",'IPC11-range","IPC7-range","IPC4-range","IPCDiversity" ,"IPCForce"]. Some may not be valid for all networks

// Canvas size
settings.save_at_the_end = false
settings.width =  1000
settings.height = 1000
settings.offset = 20 // Margin

// Clusters
settings.cluster_spreading = 150 // More = bigger and rounder contour
settings.cluster_opacity = 0.8 // [0, 1]
settings.cluster_contour = true // true = a contour line, false = a fuzzy stain
settings.cluster_contour_threshold = 0.3 // [0, 1] More = narrower contour

// Drawing nodes, labels and edges
settings.display_label = false
settings.node_size = 0.6
settings.font_size = 9
settings.font_family = 'Open Sans Condensed, sans-serif'
settings.font_weight = 300
settings.edge_color = 'rgba(200, 200, 200, 0.3)'

// --- (end of settings)

// Create the canvas
document.querySelector('#playground').innerHTML = '<div style="width:'+settings.width+'; height:'+settings.height+';"><canvas id="cnvs" width="'+settings.width+'" height="'+settings.height+'"></canvas></div>'
var canvas = document.querySelector('#cnvs')
var ctx = canvas.getContext("2d")

// Fix missing coordinates and/or colors
addMissingVisualizationData()

// Change the coordinates of the network to fit the canvas space
rescaleGraphToGraphicSpace()

// Extract the different cluster classes
var classesIndex = {}
var cl
g.nodes().forEach(function(nid){
	classesIndex[g.getNodeAttribute(nid, settings.cluster_attribute)] = true
})

// Colors
var colors = ["#5f93bc","#d27533","#b05edc","#67a43a","#da50a5","#599a75","#de4e55","#867bd3","#a3884c","#bc7590"]
var count = 0
for (cl in classesIndex) {
	if (count < colors.length) {
		classesIndex[cl] = colors[count]
	} else {
		classesIndex[cl] = '#AAA'
	}
	count++
}

// Init layers
var layers = []
for (cl in classesIndex) {
	layers.push({cl:cl})
}

// Compute pixel values
layers.forEach(function(layer){
	layer.pixelValues = (function(){

		// Compute heatmap values
		var pixelValues = new Float32Array(settings.width * settings.height)
		var i
		var x
		var y
		var n
		var d
		var value

		// Init pixel
		for (i in pixelValues) {
			pixelValues[i] = 0	
		}

		// Values from nodes
		g.nodes()
		.filter(function(nid){
			return g.getNodeAttribute(nid, settings.cluster_attribute) == layer.cl
		})
		.forEach(function(nid){
			n = g.getNodeAttributes(nid)
			for (x = Math.max(0, Math.floor(n.x - settings.cluster_spreading/2) ); x <= Math.min(settings.width, Math.floor(n.x + settings.cluster_spreading/2) ); x++ ){
				for (y = Math.max(0, Math.floor(n.y - settings.cluster_spreading/2) ); y <= Math.min(settings.height, Math.floor(n.y + settings.cluster_spreading/2) ); y++ ){
					d = Math.sqrt(Math.pow(n.x - x, 2) + Math.pow(n.y - y, 2))
					if (d < settings.cluster_spreading / 2) {
						// Compute base value: d=0 -> 1, d=spreading/2 -> 0
						value = 1 - 2 * d / settings.cluster_spreading
						// Take node size in account
						value *= n.size
						// Add value to the pixel
						i = x + settings.width * y
						pixelValues[i] = pixelValues[i] + value
					}
				}
			}
		})

		return pixelValues
	})()
})

var maxValue = d3.max(layers.map(function(layer){
	return d3.max(layer.pixelValues)
}))

// Compute layers image data
layers.forEach(function(layer){
	layer.imgd = (function(){
		// Paint heatmap
		var imgd = ctx.getImageData(0, 0, settings.width, settings.height)
		var pix = imgd.data
		var pixlen
		var i
		var value
		for ( i = 0, pixlen = pix.length; i < pixlen; i += 4 ) {
			value = layer.pixelValues[i/4] / maxValue
			var color = d3.rgb(classesIndex[layer.cl])
			if (settings.cluster_contour) {
				if (value > settings.cluster_contour_threshold) {
				  pix[i  ] = color.r // red
				  pix[i+1] = color.g // green
				  pix[i+2] = color.b // blue
				  pix[i+3] = Math.floor(settings.cluster_opacity * 255)
				}
			} else {
			  pix[i  ] = color.r // red
			  pix[i+1] = color.g // green
			  pix[i+2] = color.b // blue
			  pix[i+3] = Math.floor(settings.cluster_opacity * 255 * value)
			}
		}

		if (settings.cluster_contour) {
			// Convolute: blur
			imgd = convolute(imgd,
			[  0, .1,  0,
		    .1, .6, .1,
		     0, .1,  0 ]
	    )

			// Convolute: contour
			imgd = convolute(imgd,
			[  0, -1,  0,
		    -1,  4, -1,
		     0, -1,  0 ]
	    )

			// Convolute: blur
			imgd = convolute(imgd,
			[ .1, .3, .1,
		    .3, .8, .3,	
		    .1, .3, .1 ]
	    )
		}

    return imgd

	})()

})

// Merge layers
var imgd = ctx.createImageData(settings.width, settings.height)
var pix = imgd.data
var i
var pixlen
for ( i = 0, pixlen = pix.length; i < pixlen; i += 4 ) {
	var channel
	for (channel = 0; channel <= 2; channel++) {
		pix[i+channel] = 255
		layers.forEach(function(layer){
			pix[i+channel] -= Math.floor((255-layer.imgd.data[i+channel]) * layer.imgd.data[i+3]/255)
		})
	}
	pix[i+3] = 255
}

// Draw cluster contours
ctx.putImageData( imgd, 0, 0 )

// Draw each edge
g.edges().forEach(function(eid){
	var ns = g.getNodeAttributes(g.source(eid))
	var nt = g.getNodeAttributes(g.target(eid))

  ctx.beginPath()
  ctx.lineCap="round"
  ctx.lineJoin="round"
  ctx.strokeStyle = settings.edge_color
  ctx.fillStyle = 'rgba(0, 0, 0, 0)';
  ctx.lineWidth = settings.edge_thickness
  ctx.moveTo(ns.x, ns.y)
  ctx.lineTo(nt.x, nt.y)
  ctx.stroke()
  ctx.closePath()
})

// Draw each node
g.nodes().forEach(function(nid){
	var n = g.getNodeAttributes(nid)

  ctx.lineCap="round"
  ctx.lineJoin="round"

  if (settings.display_label) {
    ctx.font = settings.font_weight + " " + settings.font_size+"px "+settings.font_family;
    ctx.lineWidth = 4
    ctx.fillStyle = '#FFFFFF'
    ctx.strokeStyle = '#FFFFFF'
    ctx.fillText(
      n.label
    , n.x + settings.node_size * n.size * 1.4
    , n.y + 0.3 * settings.font_size
    )
    ctx.strokeText(
      n.label
    , n.x + settings.node_size * n.size * 1.4
    , n.y + 0.3 * settings.font_size
    )
    ctx.lineWidth = 0
    ctx.fillStyle = n.color
    ctx.fillText(
      n.label
    , n.x + settings.node_size * n.size * 1.4
    , n.y + 0.3 * settings.font_size
    )
  }

  ctx.beginPath()
  ctx.arc(n.x, n.y, settings.node_size * n.size, 0, 2 * Math.PI, false)
  ctx.lineWidth = 0
  ctx.fillStyle = d3.rgb(classesIndex[n[settings.cluster_attribute]]).toString()
  ctx.shadowColor = 'transparent'
  ctx.fill()
})

// Save if needed
if (settings.save_at_the_end) {
  canvas.toBlob(function(blob) {
      saveAs(blob, store.get('graphname') + "Heatmap.png");
  });
}

// Display legend
var legend = d3.select('#playground').append('div')
  .style('width', '500px')
  .style('font-family', '"Raleway", sans-serif')
  .style('background-color', '#FFF')
  .style('margin', '12px')
  .style('border', '1px solid #AAA')
  .style('padding', '12px')
legend.append('h3')
  .text('Legend')
  .style('margin-top', '0')
legend.append('h4')
  .text('Color by ' + settings.cluster_attribute)
for (cl in classesIndex) {
  var color = classesIndex[cl]
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

// ---
// Functions

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

  // Initial resize
  g.nodes().forEach(function(nid){
  	var n = g.getNodeAttributes(nid)
    n.x = settings.width / 2 + (n.x - xbarycenter) * ratio
    n.y = settings.height / 2 + (n.y - ybarycenter) * ratio
    n.size *= ratio
  })

  // Additionnal zoom resize
  if (settings.zoom_enabled) {
    xbarycenter = settings.zoom_point.x * settings.width // - settings.width / 2
    ybarycenter = settings.zoom_point.y * settings.height // - settings.height / 2
    ratio = 1/settings.zoom_window_size

    g.nodes().forEach(function(nid){
  		var n = g.getNodeAttributes(nid)
      n.x = settings.width / 2 + (n.x - xbarycenter) * ratio
      n.y = settings.height / 2 + (n.y - ybarycenter) * ratio
      n.size *= ratio
    })
  }
}

// Code from https://www.html5rocks.com/en/tutorials/canvas/imagefilters/
function convolute(pixels, weights, opaque) {
  var side = Math.round(Math.sqrt(weights.length));
  var halfSide = Math.floor(side/2);
  var src = pixels.data;
  var sw = pixels.width;
  var sh = pixels.height;
  // pad output by the convolution matrix
  var w = sw;
  var h = sh;
  var output = ctx.createImageData(w,h)
  var dst = output.data;
  // go through the destination image pixels
  var alphaFac = opaque ? 1 : 0;
  for (var y=0; y<h; y++) {
    for (var x=0; x<w; x++) {
      var sy = y;
      var sx = x;
      var dstOff = (y*w+x)*4;
      // calculate the weighed sum of the source image pixels that
      // fall under the convolution matrix
      var r=0, g=0, b=0, a=0;
      for (var cy=0; cy<side; cy++) {
        for (var cx=0; cx<side; cx++) {
          var scy = sy + cy - halfSide;
          var scx = sx + cx - halfSide;
          if (scy >= 0 && scy < sh && scx >= 0 && scx < sw) {
            var srcOff = (scy*sw+scx)*4;
            var wt = weights[cy*side+cx];
            r += src[srcOff] * wt;
            g += src[srcOff+1] * wt;
            b += src[srcOff+2] * wt;
            a += src[srcOff+3] * wt;
          }
        }
      }
      dst[dstOff] = r;
      dst[dstOff+1] = g;
      dst[dstOff+2] = b;
      dst[dstOff+3] = a + alphaFac*(255-a);
    }
  }
  return output;
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