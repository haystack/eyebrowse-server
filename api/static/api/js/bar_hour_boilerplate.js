"use strict";
var w = 780; //width
var h = 400; //height
var padding = {
    top: 40,
    right: 190,
    bottom: 40,
    left: 45
};

var stack = d3.layout.stack();

var colors_list = ["#000000", "#3300BB", "#1f77b4", "#2ca02c", "#999955", "#ff7f0e", "#ff0000", "#ff69b4", "#992299", "#551a8b", "#777777"];

//Easy colors accessible via a 10-step ordinal scale
var colors = d3.scale.category10();

var svg,
    groups,
    rects,
    xScale,
    yScale,
    xAxis,
    yAxis,
    legend,
    color_hash;

var start_time,
    end_time;

d3.json("http://eyebrowse.csail.mit.edu/api/graphs/timeline_hours?username=" + username + "&date=" + date + "&query=" + query,
    function(error, data) {
        var hour_list = data.week_hours;
        var domain_list = data.domain_list;

        start_time = data.start_time;
        end_time = data.end_time;

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

    svg.append("text")
        .attr("class", "xtext")
        .attr("x", 10)
        .attr("y", 17)
        .attr("text-anchor", "left")
        .attr("style", "font-family: Arial; font-size: 17.8px; fill: #000000; opacity: 1;")
        .style("cursor", "pointer")
        .on("click", function(d) {
            window.location.href = "http://eyebrowse.csail.mit.edu";
        })
        .text("eyebrowse.csail.mit.edu");

    if (query.length == 0) {
        var q_text = "";
    } else {
        var q_text = " | " + query;
    }
    svg.append("text")
        .attr("class", "xtext")
        .attr("x", 10)
        .attr("y", 30)
        .attr("text-anchor", "left")
        .attr("style", "font-family: Arial; font-size: 14.8px; fill: #000000; opacity: 1;")
        .text("Time spent per hour of day | " + username + " | " + start_time + ' to ' + end_time + q_text);
}



function create_scales(dataset, domain_start, domain_end, tick_x, x_tickfmt) {
    xScale = d3.scale.linear()
        .domain([domain_start, domain_end])
        .rangeRound([0, w - padding.left - padding.right]);

    yScale = d3.scale.linear()
        .domain([0,
            d3.max(dataset, function(d) {
                return d3.max(d, function(d) {
                    return d.y0 + d.y;
                });
            })
        ])
        .range([h - padding.bottom - padding.top, 0])
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
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - 5)
        .attr("x", 0 - (h / 2))
        .attr("dy", "1em")
        .attr("style", "font-family: Arial; font-size: 16.8px; fill: #000000; opacity: 1;")
        .text(y_label);

    svg.append("text")
        .attr("class", "xtext")
        .attr("x", w / 2 - padding.left)
        .attr("y", h - 5)
        .attr("text-anchor", "middle")
        .attr("style", "font-family: Arial; font-size: 16.8px; fill: #000000; opacity: 1;")
        .text(x_label);
}

function create_legend(dataset) {
    legend = svg.append("g")
        .attr("class", "legend")
        .attr("x", w - padding.right + 10)
        .attr("y", 90)
        .attr("height", 100)
        .attr("width", 100);
    svg.append("text")
        .attr("class", "legend")
        .attr("x", w - padding.right)
        .attr("y", 90)
        .attr("text-anchor", "left")
        .attr("style", "font-family: Arial; font-size: 16.8px; fill: #000000; opacity: 1;")
        .text("Top Domains Visited");

    legend.selectAll("g").data(dataset)
        .enter()
        .append('g')
        .each(function(d, i) {
            var g = d3.select(this);
            g.append("rect")
                .attr("x", w - padding.right + 10)
                .attr("y", 90 + i * 25 + 10)
                .attr("width", 10)
                .attr("height", 10)
                .style("fill", color_hash[String(i)][1]);
            g.append("text")
                .attr("x", w - padding.right + 25)
                .attr("y", 90 + i * 25 + 20)
                .attr("height", 30)
                .attr("width", 200)
                .style("fill", color_hash[String(i)][1])
                .style("font-size", "15px")
                .style("opacity", 1)
                .style("cursor", "pointer")
                .on("click", function(d) {
                    if (color_hash[String(i)][0] === "Other") {
                        return;
                    } else {
                        window.location.href = "http://" + color_hash[String(i)][0];
                    }
                })
                .style("font-family", "Arial")
                .text(color_hash[String(i)][0]);
        });

}

function transform_axes() {
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(52," + (h - padding.bottom) + ")")
        .attr("style", "font-family: Arial; font-size: 13px; fill: #000000; opacity: 1;")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + (padding.left + 5) + "," + padding.top + ")")
        .attr("style", "font-family: Arial; font-size: 13px; fill: #000000; opacity: 1;")
        .call(yAxis);
}

function set_transition() {
    rects.transition()
        .duration(function(d, i) {
            return 200 * i;
        })
        .ease("linear")
        .attr("x", function(d) {
            return xScale(new Date(d.time));
        })
        .attr("y", function(d) {
            return -(-yScale(d.y0) - yScale(d.y) + (h - padding.top - padding.bottom) * 2);
        })
        .attr("height", function(d) {
            return -yScale(d.y) + (h - padding.top - padding.bottom);
        })
        .attr("width", 15)
        .style("fill-opacity", 1);
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
        .attr("class", "rgroups")
        .attr("transform", "translate(" + padding.left + "," + (h - padding.bottom) + ")")
        .style("fill", function(d, i) {
            return color_hash[dataset.indexOf(d)][1];
        });
    // Add a rect for each data value
    rects = groups.selectAll("rect")
        .data(function(d) {
            return d;
        })
        .enter()
        .append("rect")
        .attr("width", 2)
        .style("fill-opacity", 1e-6);
}
