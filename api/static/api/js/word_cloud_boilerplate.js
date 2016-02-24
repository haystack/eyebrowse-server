"use strict";

var startTime,
    endTime;

d3.json("http://eyebrowse.csail.mit.edu/api/graphs/word_cloud?filter=" + filter + "&username=" + username + "&date=" + date + "&query=" + query,
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

var background = svg.append("g");

var vis = svg.append("g")
    .attr("transform", "translate(" + [w >> 1, h >> 1] + ")");


var wordSeparators = /[\s\u3031-\u3035\u309b\u309c\u30a0\u30fc\uff70]+/g,
    discard = /^(@|https?:|\/\/)/,
    htmlTags = /(<[^>]*?>|<script.*?<\/script>|<style.*?<\/style>|<head.*?><\/head>)/g,
    matchTwitter = /^https?:\/\/([^\.]*\.)?twitter\.com/;

function parseHTML(d) {
    parseText(d.replace(htmlTags, " ").replace(/&#(x?)([\dA-Fa-f]{1,4});/g, function(d, hex, m) {
        return String.fromCharCode(+((hex ? "0x" : "") + m));
    }).replace(/&\w+;/g, " "));
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

    svg.append("text")
        .attr("class", "xtext")
        .attr("x", 10)
        .attr("y", h - 35)
        .attr("text-anchor", "left")
        .attr("style", "font-family: Arial; font-size: 25.8px; fill: #000000; opacity: 1;")
        .style("cursor", "pointer")
        .on("click", function(d) {
            window.location.href = "http://eyebrowse.csail.mit.edu";
        })
        .text("eyebrowse.csail.mit.edu");
    svg.append("text")
        .attr("class", "xtext")
        .attr("x", 10)
        .attr("y", h - 15)
        .attr("text-anchor", "left")
        .attr("style", "font-family: Arial; font-size: 20.8px; fill: #000000; opacity: 1;")
        .text("Word cloud of page titles | " + username + " | " + date + " | " + query);

}

function load(f) {
    if (f === null) {
        return;
    } else {
        if (query !== null) {
            window.location.href = "http://eyebrowse.csail.mit.edu/users/amyzhang?query=" + query + " " + f + "&date=" + date;
        } else {
            window.location.href = "http://eyebrowse.csail.mit.edu/users/amyzhang?query=" + f + "&date=" + date;
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
        .style("opacity", 0.7);

    text.style("font-family", function(d) {
        return d.font;
    })
        .style("fill", function(d) {
            return fill(d.text.toLowerCase());
        })
        .text(function(d) {
            return d.text;
        });
}
