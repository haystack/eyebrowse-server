"use strict";

google.load("visualization", "1", {
    packages: ["corechart"]
});
google.setOnLoadCallback(drawChart1);

function drawChart1() {

    var jvals = $("#piechart1").text();
    if (jvals.length > 2) {
        var obj = $.parseJSON(jvals);
        var arr = [
            ["Domain", "Link", "Visits"]
        ];
        for (var key in obj) {
            if (obj.hasOwnProperty(key)) {
                arr.push([key, "http://" + key, Math.round((obj[key] / 60000.0) * 100) / 100]);
            }
        }

        $("#piechart1").text("");

        var data = google.visualization.arrayToDataTable(arr);

        var view = new google.visualization.DataView(data);
        view.setColumns([0, 2]);

        var options = {
            backgroundColor: "transparent",
            "width": 480,
            "height": 200,
            //              legend: "none",
        };

        var chart = new google.visualization.PieChart(document.getElementById("piechart1"));
        chart.draw(view, options);

        var selectHandler = function(e) {
            window.location = data.getValue(chart.getSelection()[0].row, 1);
        };

        // Add our selection handler.
        google.visualization.events.addListener(chart, "select", selectHandler);

        $("#piechart1").css("visibility", "visible");

    } else {
        $("#piechart1").remove();
    }
}

google.load("visualization", "1", {
    packages: ["corechart"]
});
google.setOnLoadCallback(drawChart2);

function drawChart2() {

    var jvals = $("#piechart2").text();
    if (jvals.length > 2) {
        var obj = $.parseJSON(jvals);
        var arr = [
            ["Domain", "Link", "Visits"]
        ];
        for (var key in obj) {
            if (obj.hasOwnProperty(key)) {
                arr.push([key, "http://" + key, Math.round((obj[key] / 60000.0) * 100) / 100]);
            }
        }

        $("#piechart2").text("");

        var data = google.visualization.arrayToDataTable(arr);

        var view = new google.visualization.DataView(data);
        view.setColumns([0, 2]);

        var options = {
            backgroundColor: "transparent",
            "width": 480,
            "height": 200,
            //legend: "none",
        };

        var chart = new google.visualization.PieChart(document.getElementById("piechart2"));
        chart.draw(view, options);

        var selectHandler = function(e) {
            window.location = data.getValue(chart.getSelection()[0].row, 1);
        };

        // Add our selection handler.
        google.visualization.events.addListener(chart, "select", selectHandler);

        $("#piechart2").css("visibility", "visible");

    } else {
        $("#piechart2").remove();
    }
}
