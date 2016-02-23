"use strict";

var startTime,
    endTime;

var username = getURLUsername();
var date = getURLParameter("date");
var query = getURLParameter("query");
var filter = getURLParameter("filter");

d3.json("/api/graphs/word_cloud?filter=" + filter + "&username=" + username + "&date=" + date + "&query=" + query,
    function(error, data) {
        var wordList = data.week_words;

        startTime = data.start_time;
        endTime = data.end_time;
        parseText(wordList);

    });

var fontSize = d3.scale.log().range([10, 100]);

var fill = d3.scale.category20();

var w = Math.min(750, $(window).width()),
    h = 400;

var words = [],
    max,
    scale = 1,
    complete = 0,
    keyword = "",
    tags,
    fontSize,
    maxLength = 30,
    fetcher;

var layout = d3.layout.cloud()
    .timeInterval(10)
    .size([w, h])
    .fontSize(function(d) {
        return fontSize(+d.value);
    })
    .text(function(d) {
        return d.key;
    })
    .on("end", draw);

var svg = d3.select("#wordle").append("svg")
    .attr("width", w)
    .attr("height", h);


var background = svg.append("g"),
    vis = svg.append("g")
        .attr("transform", "translate(" + [w >> 1, h >> 1] + ")");

d3.select("#download-png").on("click", downloadPNG);

d3.select("#get-widget").on("click", showWidget);

var wordSeparators = /[\s\u3031-\u3035\u309b\u309c\u30a0\u30fc\uff70]+/g,
    discard = /^(@|https?:|\/\/)/,
    htmlTags = /(<[^>]*?>|<script.*?<\/script>|<style.*?<\/style>|<head.*?><\/head>)/g,
    matchTwitter = /^https?:\/\/([^\.]*\.)?twitter\.com/;

function parseHTML(d) {
    parseText(d.replace(htmlTags, " ").replace(/&#(x?)([\dA-Fa-f]{1,4});/g, function(d, hex, m) {
        return String.fromCharCode(+((hex ? "0x" : "") + m));
    }).replace(/&\w+;/g, " "));
}

function showWidget() {
    var $collapse = $("#widget-code-word");
    query = query || "";
    username = username || "";
    date = date || "";
    filter = filter || "";

    $("#widget-code-text-word").text("<div id=\"wordle\"></div>\n" +
        "<script src=\"http://code.jquery.com/jquery-1.11.2.min.js\"></script>\n" +
        "<script src=\"http://d3js.org/d3.v3.min.js\" charset=\"utf-8\"></script>\n" +
        "<script src=\"http://eyebrowse.csail.mit.edu/static/common/js/d3.layout.cloud.min.js\" charset=\"utf-8\"></script>\n" +
        "<script src=\"http://eyebrowse.csail.mit.edu/api/graphs/js/word_cloud?filter=" + filter + "&username=" + username + "&date=" + date + "&query=" + query + "\" charset=\"utf-8\"></script>");

    $collapse.collapse("toggle");
}

function downloadPNG() {
    var canvas = document.createElement("canvas"),
        c = canvas.getContext("2d");
    canvas.width = w;
    canvas.height = h;
    c.translate(w >> 1, h >> 1);
    c.scale(scale, scale);
    words.forEach(function(word, i) {
        c.save();
        c.translate(word.x, word.y);
        c.rotate(word.rotate * Math.PI / 180);
        c.textAlign = "center";
        c.fillStyle = fill(word.text.toLowerCase());
        c.font = word.size + "px " + word.font;
        c.fillText(word.text, 0, 0);
        c.restore();
    });

    c.restore();
    c.textAlign = "start";
    c.fillStyle = "#000000";
    c.font = "16px Arial";
    c.fillText("eyebrowse.csail.mit.edu", (w / 2) * -1 + 20, (h / 2) - 30);
    c.save();


    var text = "Word cloud of page titles | Collected from " + username + "'s web visits";
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
    c.fillText(text, (w / 2) * -1 + 20, (h / 2) - 15);
    c.save();

    var a = document.createElement("a");
    a.download = "image.png";
    a.href = canvas.toDataURL("image/png");
    a.click();
}



function parseText(wordList) {
    tags = {};
    var cases = {};
    wordList.forEach(function(word) {
        if (discard.test(word[0])) {
            return;
        }
        var wordShort = word[0].substr(0, maxLength);
        cases[wordShort] = wordShort;
        tags[wordShort] = word[1];
    });
    tags = d3.entries(tags).sort(function(a, b) {
        return b.value - a.value;
    });
    tags.forEach(function(d) {
        d.key = cases[d.key];
    });
    generate();
}

function generate() {
    layout
        .font("Arial")
        .spiral("archimedean");
    fontSize = d3.scale.sqrt().range([10, 100]);
    if (tags.length) {
        fontSize.domain([+tags[tags.length - 1].value || 1, +tags[0].value]);
    }
    complete = 0;
    words = [];
    layout.stop().words(tags.slice(0, max = Math.min(tags.length, +250))).start();

}

function load(f) {
    if (f === null) {
        return;
    } else {
        if (query !== null) {
        	if (filter != null) {
        		window.location.href = "http://eyebrowse.csail.mit.edu/livestream/?filter=" + filter + "&query=" + query + " " + f + "&date=" + date;
        	} else {
            	window.location.href = "http://eyebrowse.csail.mit.edu/users/" + username + "?query=" + query + " " + f + "&date=" + date;
        	}
        } else {
        	if (filter != null) {
        		window.location.href = "http://eyebrowse.csail.mit.edu/livestream/?filter=" + filter + "&query=" + f + "&date=" + date;
        	} else {
            	window.location.href = "http://eyebrowse.csail.mit.edu/users/" + username + "?query=" + f + "&date=" + date;
        	}
        }

    }
}

function draw(data, bounds) {
    scale = bounds ? Math.min(
        w / Math.abs(bounds[1].x - w / 2),
        w / Math.abs(bounds[0].x - w / 2),
        h / Math.abs(bounds[1].y - h / 2),
        h / Math.abs(bounds[0].y - h / 2)) / 2 : 1;
    words = data;
    var text = vis.selectAll("text")
        .data(words, function(d) {
            return d.text.toLowerCase();
        });

    text.transition()
        .duration(1000)
        .attr("transform", function(d) {
            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .style("font-size", function(d) {
            return d.size + "px";
        });

    text.enter().append("text")
        .attr("text-anchor", "middle")
        .attr("transform", function(d) {
            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .style("font-size", function(d) {
            return d.size + "px";
        })
        .style("cursor", "pointer")
        .on("click", function(d) {
            load(d.text);
        })
        .style("opacity", 1e-6)
        .transition()
        .duration(1000)
        .style("opacity", 1);

    text.style("font-family", function(d) {
        return d.font;
    })
        .style("fill", function(d) {
            return fill(d.text.toLowerCase());
        })
        .text(function(d) {
            return d.text;
        });

    var exitGroup = background.append("g")
        .attr("transform", vis.attr("transform"));

    var exitGroupNode = exitGroup.node();

    text.exit().each(function() {
        exitGroupNode.appendChild(this);
    });

    exitGroup.transition()
        .duration(1000)
        .style("opacity", 1e-6)
        .remove();

    vis.transition()
        .delay(1000)
        .duration(750)
        .attr("transform", "translate(" + [w >> 1, h >> 1] + ")scale(" + scale + ")");


}
