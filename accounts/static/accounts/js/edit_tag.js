"use strict";

function rmTag(e) {
    var $target = $(e.currentTarget);
    var domain = $target.data("url");
    var tag = $target.data("tag");
    $.post("/delete_tag", {
        "tag": tag,
        "domain": domain,
    });
    window.location.reload();
}

function colorTag(e) {
    var $target = $(e.currentTarget);
    var tag = $target.data("tag");
    $.post("/color_tag", {
        "tag": tag,
    });
    window.location.reload();
}

$(function() {
    $(".tags").on("click", ".rm-tag", rmTag);

    $(".delete-tag").click(rmTag);

    $(".change-color-tag").click(colorTag);
});
