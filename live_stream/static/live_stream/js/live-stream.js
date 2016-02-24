"use strict";

$(function() {

    if (getURLParameter("sort") === "time") {
        var liveStream = new LiveStreamPing({
            "filterFunc": getURLParameter,
            "defaultFilter": "following",
            "searchParams": {
                "template": "history_item_template_new",
                "query": $(".search-bar").val(),
                "date": $(".date-search-bar").val(),
            },
        }, liveStreamCallback);
    }

    calculateStats();

    $(".history-container").on("click", ".connection", follow);

});


$("#hide-visited-domain").click(function(){
    $('.eye-hist-visited').toggle();
    $(this).text(function(i, text){
        return text == "Hide Visited" ? "Show Visited" : "Hide Visited";
    })
});
