
$(document).ready(function(){
	
	
	var hour_list = JSON.parse($('#stackedbar-chart').text());
	var domain_list = JSON.parse($('#domain_list').text());

	$('#stackedbar-chart').text("");
	$("#stackedbar-chart").css({'visibility': "visible"});
	
	
	var w = 780;                        //width
	var h = 400;                        //height
	var padding = {top: 40, right: 180, bottom: 40, left:45};
	//Set up stack method
	var stack = d3.layout.stack();

	var dataset = hour_list;
	stack(dataset);

	var color_hash = {
		    0 : [domain_list[0], "#1f77b4"],
			1 : [domain_list[1], "#2ca02c"],
			2 : [domain_list[2], "#ff7f0e"],
		    3 : [domain_list[3], "#ff0000"],
			4 : [domain_list[4], "#ff69b4"],
			5 : ["Other", "#551a8b"],

			};
			

			//Set up scales
			var xScale = d3.scale.linear()
				.domain([0,24])
				.rangeRound([0, w - padding.left - padding.right]);

			var yScale = d3.scale.linear()
				.domain([0,				
					d3.max(dataset, function(d) {
						return d3.max(d, function(d) {
							return d.y0 + d.y;
						});
					})
				])
				.range([h - padding.bottom - padding.top,0]);

			var xAxis = d3.svg.axis()
						   .scale(xScale)
						   .orient("bottom")
						   .ticks(24);

			var yAxis = d3.svg.axis()
						   .scale(yScale)
						   .orient("left")
						   .ticks(10);



			//Easy colors accessible via a 10-step ordinal scale
			var colors = d3.scale.category10();

			//Create SVG element
			var svg = d3.select("#stackedbar-chart")
						.append("svg")
						.attr("width", w)
						.attr("height", h);

			// Add a group for each row of data
			var groups = svg.selectAll("g")
				.data(dataset)
				.enter()
				.append("g")
				.attr("class","rgroups")
				.attr("transform","translate("+ padding.left + "," + (h - padding.bottom) +")")
				.style("fill", function(d, i) {
					return color_hash[dataset.indexOf(d)][1];
				});

			// Add a rect for each data value
			var rects = groups.selectAll("rect")
				.data(function(d) { return d; })
				.enter()
				.append("rect")
				.attr("width", 2)
				.style("fill-opacity",1e-6);


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

				svg.append("g")
					.attr("class","x axis")
					.attr("transform","translate(50," + (h - padding.bottom) + ")")
					.call(xAxis);


				svg.append("g")
					.attr("class","y axis")
					.attr("transform","translate(" + (padding.left + 5) + "," + padding.top + ")")
					.call(yAxis);

				// adding legend

				var legend = svg.append("g")
								.attr("class","legend")
								.attr("x", w - padding.right + 5)
								.attr("y", 25)
								.attr("height", 100)
								.attr("width",100);

				legend.selectAll("g").data(dataset)
					  .enter()
					  .append('g')
					  .each(function(d,i){
					  	var g = d3.select(this);
					  	g.append("rect")
					  		.attr("x", w - padding.right + 5)
					  		.attr("y", i*25 + 10)
					  		.attr("width", 10)
					  		.attr("height",10)
					  		.style("fill",color_hash[String(i)][1]);

					  	g.append("text")
					  	 .attr("x", w - padding.right + 20)
					  	 .attr("y", i*25 + 20)
					  	 .attr("height",30)
					  	 .attr("width",200)
					  	 .style("fill",color_hash[String(i)][1])
					  	 .text(color_hash[String(i)][0]);
					  });

				svg.append("text")
				.attr("transform","rotate(-90)")
				.attr("y", 0 - 5)
				.attr("x", 0-(h/2))
				.attr("dy","1em")
				.text("Number of Minutes");

			svg.append("text")
			   .attr("class","xtext")
			   .attr("x",w/2 - padding.left)
			   .attr("y",h - 5)
			   .attr("text-anchor","middle")
			   .text("Hour in the Day");


		});