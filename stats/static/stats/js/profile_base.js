"use strict";

$(function() {
    calculateStats();
    makeTip(".fav-site", $(".fav-site").data("content"), "bottom", "hover");
    $(".btn-prof-header").click(follow);
});
