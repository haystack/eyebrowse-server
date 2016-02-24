"use strict";

d3.json("/api/graphs/timeline_hours?filter=" + filter + "&username=" + username + "&date=" + date + "&query=" + query,
    function(error, data) {
        var hourList = data.week_hours;
        var domainList = data.domain_list;

        colorHash = [];

        for (var i = 0; i < domainList.length; i++) {
            colorHash.push([domainList[i], colorsList[i]]);
        }
        if (domainList.length === 10) {
            colorHash.push(["Other", colorsList[10]]);
        }

        stack(hourList);

        drawSVGHour(hourList);

    });

function drawSVGHour(dataset) {
    createScales(dataset, -0.35, 23.4, 23, function(d, i) {
        return d;
    });
    drawSVG(dataset, "#stackedbar-chart");
    setTransition();
    transformAxes();
    createLegend(dataset);
    drawAxisLabels("Hour in the Day", "Number of Minutes");
}
