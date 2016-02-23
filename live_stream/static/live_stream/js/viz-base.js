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

var colorsList = ["#000000", "#3300BB", "#1f77b4", "#2ca02c", "#999955", "#ff7f0e", "#ff0000", "#ff69b4", "#992299", "#551a8b", "#777777"];

//Easy colors accessible via a 10-step ordinal scale
var colors = d3.scale.category10();

var username = getURLUsername();
var date = getURLParameter("date");
var query = getURLParameter("query");
var filter = getURLParameter("filter");

var svg,
    groups,
    rects,
    xScale,
    yScale,
    xAxis,
    yAxis,
    legend,
    colorHash;


d3.select("#download-bar-png").on("click", function() {
    downloadbarPNG(1);
});

d3.select("#download-bar2-png").on("click", function() {
    downloadbarPNG(2);
});


d3.select("#get-widget-bar").on("click", function() {
    showBarWidget(1);
});

d3.select("#get-widget-bar2").on("click", function() {
    showBarWidget(2);
});

function showBarWidget(version) {
    var $collapse;
    var apiCall;
    var textBox;

    if (version === 1) {
        $collapse = $("#widget-code-bar");
        apiCall = "bar_hour";
        textBox = "#widget-code-text-bar";
    } else {
        $collapse = $("#widget-code-bar2");
        apiCall = "bar_day";
        textBox = "#widget-code-text-bar2";
    }

    query = query || "";
    username = username || "";
    date = date || "";

    if (version === 1) {
        $(textBox).text("<div id=\"stackedbar-chart\"></div>\n" +
            "<script src=\"http://code.jquery.com/jquery-1.11.2.min.js\"></script>\n" +
            "<script src=\"http://d3js.org/d3.v3.min.js\" charset=\"utf-8\"></script>\n" +
            "<script src=\"http://eyebrowse.csail.mit.edu/api/graphs/js/" + apiCall + "?filter=" + filter + "&username=" + username + "&date=" + date + "&query=" + query + "\" charset=\"utf-8\"></script>");
    } else {
        $(textBox).text("<div id=\"stackedbar-chart2\"></div>\n" +
            "<script src=\"http://code.jquery.com/jquery-1.11.2.min.js\"></script>\n" +
            "<script src=\"http://d3js.org/d3.v3.min.js\" charset=\"utf-8\"></script>\n" +
            "<script src=\"http://eyebrowse.csail.mit.edu/api/graphs/js/" + apiCall + "?filter=" + filter + "&username=" + username + "&date=" + date + "&query=" + query + "\" charset=\"utf-8\"></script>");
    }
    $collapse.collapse("toggle");
}

function downloadbarPNG(version) {

    var xml;
    if (version === 1) {
        xml = document.getElementById("stackedbar-chart").firstElementChild;
    } else {
        xml = document.getElementById("stackedbar-chart2").firstElementChild;
    }

    var img = new Image(),
        serializer = new XMLSerializer(),
        svgStr = serializer.serializeToString(xml);

    img.src = "data:image/svg+xml;base64," + window.btoa(svgStr);

    var canvas = document.createElement("canvas");
    canvas.width = w;
    canvas.height = h;
    var c = canvas.getContext("2d");
    c.drawImage(img, 0, 0, w, h);

    c.restore();
    c.textAlign = "start";
    c.fillStyle = "#000000";
    c.font = "16px Arial";
    c.fillText("eyebrowse.csail.mit.edu", 0, 13);
    c.save();

    var text;
    if (version === 1) {
        text = "Time spent per hour of day | Collected from " + username + "'s web visits";
    } else {
        text = "Time spent per day of week | Collected from " + username + "'s web visits";
    }

    if (startTime !== null && endTime !== null) {
        text = text + " | " + startTime + " to " + endTime;
    }
    if (query !== null) {
        text = text + " | filtered by \"" + query + "\"";
    }
    c.restore();
    c.textAlign = "start";
    c.fillStyle = "#000000";
    c.font = "14px Arial";
    c.fillText(text, 0, 28);
    c.save();

    var a = document.createElement("a");
    a.download = "image.png";
    a.href = canvas.toDataURL("image/png");
    a.click();
}



function createScales(dataset, domainStart, domainEnd, tickX, xTickfmt) {
    xScale = d3.scale.linear()
        .domain([domainStart, domainEnd])
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
        .ticks(tickX)
        .tickFormat(xTickfmt);

    yAxis = d3.svg.axis()
        .scale(yScale)
        .orient("left")
        .ticks(10);
}

function drawAxisLabels(xLabel, yLabel) {
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - 5)
        .attr("x", 0 - (h / 2))
        .attr("dy", "1em")
        .attr("style", "font-family: Arial; font-size: 16.8px; fill: #000000; opacity: 1;")
        .text(yLabel);

    svg.append("text")
        .attr("class", "xtext")
        .attr("x", w / 2 - padding.left)
        .attr("y", h - 5)
        .attr("text-anchor", "middle")
        .attr("style", "font-family: Arial; font-size: 16.8px; fill: #000000; opacity: 1;")
        .text(xLabel);
}

function createLegend(dataset) {
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
        .append("g")
        .each(function(d, i) {
            var g = d3.select(this);
            g.append("rect")
                .attr("x", w - padding.right + 10)
                .attr("y", 90 + i * 25 + 10)
                .attr("width", 10)
                .attr("height", 10)
                .style("fill", colorHash[String(i)][1]);
            g.append("text")
                .attr("x", w - padding.right + 25)
                .attr("y", 90 + i * 25 + 20)
                .attr("height", 30)
                .attr("width", 200)
                .style("fill", colorHash[String(i)][1])
                .style("font-size", "15px")
                .style("opacity", 1)
                .style("cursor", "pointer")
                .on("click", function(d) {
                    if (colorHash[String(i)][0] === "Other") {
                        return;
                    } else {
                        window.location.href = "http://" + colorHash[String(i)][0];
                    }
                })
                .style("font-family", "Arial")
                .text(colorHash[String(i)][0]);
        });

}

function transformAxes() {
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

function setTransition() {
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



function drawSVG(dataset, element) {
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
            return colorHash[dataset.indexOf(d)][1];
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
