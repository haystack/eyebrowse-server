
d3.json("/api/graphs/timeline_hours?username=" + username + "&date=" + date + "&query=" + query,
	function(error, data) {
		var hour_list = data.week_hours;
		var domain_list = data.domain_list;
		
		color_hash = {
		    0 : [domain_list[0], "#1f77b4"],
			1 : [domain_list[1], "#2ca02c"],
			2 : [domain_list[2], "#ff7f0e"],
		    3 : [domain_list[3], "#ff0000"],
			4 : [domain_list[4], "#ff69b4"],
			5 : ["Other", "#551a8b"],
			};

		stack(hour_list);
		
		draw_SVG_hour(hour_list);
		
	});

function draw_SVG_hour(dataset) {
	create_scales(dataset, -.35, 23.4, 23, function(d,i) {return d;});
	draw_SVG(dataset, "#stackedbar-chart");
	set_transition();
	transform_axes();
	create_legend(dataset);
 	draw_axis_labels("Hour in the Day","Number of Minutes");
}
			