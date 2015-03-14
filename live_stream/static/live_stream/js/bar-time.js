"use strict";

d3.json("/api/graphs/timeline_hours?username=" + username + "&date=" + date + "&query=" + query,
    function(error, data) {
        var hour_list = data.week_hours;
        var domain_list = data.domain_list;

        color_hash = [];

        for (var i = 0; i < domain_list.length; i++) {
            color_hash.push([domain_list[i], colors_list[i]]);
        }
        if (domain_list.length == 10) {
            color_hash.push(["Other", colors_list[10]]);
        }

        stack(hour_list);

        draw_SVG_hour(hour_list);

    });

function draw_SVG_hour(dataset) {
    create_scales(dataset, -.35, 23.4, 23, function(d, i) {
        return d;
    });
    draw_SVG(dataset, "#stackedbar-chart");
    set_transition();
    transform_axes();
    create_legend(dataset);
    draw_axis_labels("Hour in the Day", "Number of Minutes");
}
