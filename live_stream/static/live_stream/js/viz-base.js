var w = 780;                        //width
var h = 400;                        //height
var padding = {top: 40, right: 190, bottom: 40, left:45};

var stack = d3.layout.stack();
		
//Easy colors accessible via a 10-step ordinal scale
var colors = d3.scale.category10();

var username = getURLUsername();
var date = getURLParameter("date");
var query = getURLParameter("query");

var svg,
	groups,
	rects,
	xScale,
	yScale,
	xAxis,
	yAxis,
	legend,
	color_hash;
	
	
function create_scales(dataset, domain_start, domain_end, tick_x, x_tickfmt) {
	xScale = d3.scale.linear()
		.domain([domain_start,domain_end])
		.rangeRound([0, w - padding.left - padding.right]);
		
	yScale = d3.scale.linear()
		.domain([0,				
			d3.max(dataset, function(d) {
				return d3.max(d, function(d) {
					return d.y0 + d.y;
				});
			})
		])
		.range([h - padding.bottom - padding.top,0])
		.nice();
		
	xAxis = d3.svg.axis()
	   .scale(xScale)
	   .orient("bottom")
	   .ticks(tick_x)
	   .tickFormat(x_tickfmt);
	
	yAxis = d3.svg.axis()
	   .scale(yScale)
	   .orient("left")
	   .ticks(10);	
}

function draw_axis_labels(x_label, y_label) {
	svg.append("text")
		.attr("transform","rotate(-90)")
		.attr("y", 0 - 5)
		.attr("x", 0-(h/2))
		.attr("dy","1em")
		.text(y_label);

	svg.append("text")
	   .attr("class","xtext")
	   .attr("x",w/2 - padding.left)
	   .attr("y",h - 5)
	   .attr("text-anchor","middle")
	   .text(x_label);
}

function create_legend(dataset) {
	legend = svg.append("g")
					.attr("class","legend")
					.attr("x", w - padding.right + 10)
					.attr("y", 25)
					.attr("height", 100)
					.attr("width",100);

	legend.selectAll("g").data(dataset)
		  .enter()
		  .append('g')
		  .each(function(d,i){
		  	var g = d3.select(this);
		  	g.append("rect")
		  		.attr("x", w - padding.right + 10)
		  		.attr("y", i*25 + 10)
		  		.attr("width", 10)
		  		.attr("height",10)
		  		.style("fill",color_hash[String(i)][1]);
		  	g.append("text")
		  	 .attr("x", w - padding.right + 25)
		  	 .attr("y", i*25 + 20)
		  	 .attr("height",30)
		  	 .attr("width",200)
		  	 .style("fill",color_hash[String(i)][1])
		  	 .text(color_hash[String(i)][0]);
	  	  });

}

function transform_axes() {
	svg.append("g")
		.attr("class","x axis")
		.attr("transform","translate(52," + (h - padding.bottom) + ")")
		.call(xAxis);

	svg.append("g")
		.attr("class","y axis")
		.attr("transform","translate(" + (padding.left + 5) + "," + padding.top + ")")
		.call(yAxis);
}

function set_transition() {
	rects.transition()
	    .duration(function(d,i){
	    	 return 200 * i;
	    })
	    .ease("linear")
	    .attr("x", function(d) {
			return xScale(new Date(d.time));
		})
		.attr("y", function(d) {
			return -(- yScale(d.y0) - yScale(d.y) + (h - padding.top - padding.bottom)*2);
		})
		.attr("height", function(d) {
			return -yScale(d.y) + (h - padding.top - padding.bottom);
		})
		.attr("width", 15)
		.style("fill-opacity",1);
}

function draw_SVG(dataset, element) {
	svg = d3.select(element)
		.append("svg")
		.attr("width", w)
		.attr("height", h);
	// Add a group for each row of data
	groups = svg.selectAll("g")
		.data(dataset)
		.enter()
		.append("g")
		.attr("class","rgroups")
		.attr("transform","translate("+ padding.left + "," + (h - padding.bottom) +")")
		.style("fill", function(d, i) {
			return color_hash[dataset.indexOf(d)][1];
		});
	// Add a rect for each data value
	rects = groups.selectAll("rect")
		.data(function(d) { return d; })
		.enter()
		.append("rect")
		.attr("width", 2)
		.style("fill-opacity",1e-6);
}
