"use strict";

function whitelistAdd(e, d) {
    var button = $(this);
    var url = button.data("url");
    $.post("/api/whitelist/add/", {
            "form_type": "whitelist",
            "whitelist": url
        },
        function(res) {
            if (res.success) {
                button.next("span").show();
            } else {
                console.log(res);
            }
        });
    return false;
}

function followAdd(e, d) {
    var button = $(this);
    var username = button.data("username");
    $.post("/api/whitelist/add/", {
            "form_type": "whitelist",
            "whitelist": url // TODO (xxx): seems like a bug..
        },
        function(res) {
            if (res.success) {
                button.next("span").show();
            } else {
                console.log(res);
            }
        });
    return false;
}

$(function() {
    $("#to-follow").on("click", ".follow-add", follow);
    $(".whitelist-add").on("click", whitelistAdd);
});
