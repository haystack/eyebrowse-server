"use strict";

$(function() {

    //set tool tips for truncated data
    setTips(".cut-content");

    var liveStream = new LiveStreamPing({
        "filterFunc": nullFilter,
        "defaultFilter": "none",
        "searchParams": {
            "template": "history_item_template_new",
            "username": profileUsername,
            "orderBy": "end_time",
            "direction": "hl",
            "filter": "",
            "query": $(".search-bar").val(),
            "date": $(".date-search-bar").val(),
        },
    }, liveStreamCallback);
});
