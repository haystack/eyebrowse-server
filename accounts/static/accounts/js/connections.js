"use strict";

$(function() {
    // following tab
    $("#following").on("click", ".connection", follow);
    listFilter($(".following-body"));

    // followers tab
    $("#followers").on("click", ".connection", follow);
    listFilter($(".followers-body"));
});
