"use strict";

function whitelistAdd(e, d) {
    var button = $(this);
    var url = button.data("url");
    var $icon = $(e.currentTarget).children();
    var type = $icon.data("type");

    if (type === "add-whitelist") {
        $.post("/api/whitelist/add/", {
                "form_type": "whitelist",
                "whitelist": url
            },
            function(res) {
                if (res.success) {
                    $.each($(".whitelist-add"), function(index, item) {
                        var $item = $(item).children();
                        if ($item.data("url") === $icon.data("url")) {
                            swapWhitelistClass($item, type);
                            button.attr("id", res.data.id);
                        }
                    });
                }
            });
    } else {
        var id = button.attr("id");
        console.log(id);
        $.ajax({
            url: getApiURL("whitelist", id),
            type: "DELETE",
            success: function(res) {
                $.each($(".whitelist-add"), function(index, item) {
                    var $item = $(item).children();
                    if ($item.data("url") === $icon.data("url")) {
                        swapWhitelistClass($item, type);
                    }
                });
            }
        });

    }
    return false;
}

function swapWhitelistClass(icon, type) {
    var $icon = $(icon);
    var text;
    if (type === "add-whitelist") {
        $icon.attr("data-type", "rm-whitelist");
        $icon.removeClass("glyphicon-ok").addClass("glyphicon-remove");
        text = $icon.parent().html().replace("Whitelist", "Whitelisted");
        $icon.parent().html(text);
    } else {
        $icon.attr("data-type", "add-whitelist");
        $icon.removeClass("glyphicon-remove").addClass("glyphicon-ok");
        text = $icon.parent().html().replace("Whitelisted", "Whitelist");
        $icon.parent().html(text);
    }
}

$(function() {
    $(".connection").on("click", follow);
    $(".whitelist-add").on("click", whitelistAdd);
});
