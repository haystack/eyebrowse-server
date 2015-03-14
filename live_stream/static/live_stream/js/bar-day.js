"use strict";

var week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

d3.json("/api/graphs/timeline_days?username=" + username + "&date=" + date + "&query=" + query,
    function(error, data) {
        var dayList = data.week_days;
        var domainList = data.domain_list;

        var colorHash = [];

        for (var i = 0; i < domainList.length; i++) {
            colorHash.push([domainList[i], colorsList[i]]);
        }
        if (domainList.length === 10) {
            colorHash.push(["Other", colorsList[10]]);
        }

        stack(dayList);

        drawSVGDay(dayList);

    });

function drawSVGDay(dataset) {
    var tickfmt = function(d, i) {
        return week[d];
    };
    createScales(dataset, -0.3, 7, 7, tickfmt);
    drawSVG(dataset, "#stackedbar-chart2");
    setTransition();
    transformAxes();
    createLegend(dataset);
    drawAxisLabels("Day in the Week", "Number of Minutes");
}
