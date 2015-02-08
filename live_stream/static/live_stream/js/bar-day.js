var week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

d3.json("/api/graphs/timeline_days?username=" + username + "&date=" + date + "&query=" + query,
	function(error, data) {
		var day_list = data.week_days;
		var domain_list = data.domain_list;

		color_hash = [];
		
		for (var i=0;i<domain_list.length;i++) {
			color_hash.push([domain_list[i], colors_list[i]]);
		}
		if (domain_list.length == 5) {
			color_hash.push(["Other", colors_list[5]]);
		}

		stack(day_list);
		
		draw_SVG_day(day_list);
		
	});

function draw_SVG_day(dataset) {
	var tickfmt = function(d, i){ return week[d];};
	create_scales(dataset, -.3, 7, 7, tickfmt);
	draw_SVG(dataset, "#stackedbar-chart2");
	set_transition();
	transform_axes();
	create_legend(dataset);
 	draw_axis_labels("Day in the Week","Number of Minutes");
}
			