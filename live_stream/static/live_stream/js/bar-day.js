var week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

d3.json("/api/graphs/timeline_days?username=" + username + "&date=" + date + "&query=" + query,
	function(error, data) {
		var day_list = data.week_days;
		var domain_list = data.domain_list;
		
		console.log(data);
		
		color_hash = {
		    0 : [domain_list[0], "#1f77b4"],
			1 : [domain_list[1], "#2ca02c"],
			2 : [domain_list[2], "#ff7f0e"],
		    3 : [domain_list[3], "#ff0000"],
			4 : [domain_list[4], "#ff69b4"],
			5 : ["Other", "#551a8b"],
			};

		stack(day_list);
		
		draw_SVG_day(day_list);
		
	});

function draw_SVG_day(dataset) {
	var tickfmt = function(d, i){ return week[d];};
	create_scales(dataset, 0, 7, 7, tickfmt);
	draw_SVG(dataset, "#stackedbar-chart2");
	set_transition();
	transform_axes();
	create_legend(dataset);
 	draw_axis_labels("Day in the Week","Number of Minutes");
}
			