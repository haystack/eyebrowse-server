"use strict";

function setFade() {

    var fadeTime = 8000; //8 seconds
    var $popup = $("#info-box");

    var fadePopup = setTimeout(function() {
        fade($popup)
    }, fadeTime);

    $popup.hover(function() {
        clearInterval(fadePopup);
        $popup.stop();
        $popup.css("opacity", 1.0);
    });

    $popup.mouseleave(function() {
        fadePopup = setTimeout(function() {
            fade($popup);
        }, fadeTime);
    });
}

function passMessage(action, type) {
    $("#info-box").remove();
    var message = {
        "action": action,
        "type": type,
    };
    window.parent.postMessage(JSON.stringify(message), "*")
}


function fade(el) {
    var $popup = $(".popup");
    el.fadeOut(1000, function() {
        $popup.animate({
            "top": $("#info-box").css("top") - 120
        }, 500);
        passMessage("fade");
    });
}

function clickHandle(e) {
    var action = $(e.target).data("action");
    var type = $(e.target).data("type");
    passMessage(action, type);
    passMessage("fade"); //remove iframe on btn click
}

$(document).ready(function() {
    var logged_in = $("#logged-in").text();

    if (logged_in == "False") {
        passMessage("fade");
    }

    var num_img = $("#info-box img").length;
    var text = $.trim($("#message").text());

    if (num_img > 0) {
        $(".bubble").css("visibility", "visible");
        setFade();
        var num = (num_img * 24) + 10;
        $("#info-box").css("width", num + 'px');
        $("#allow-btn").click(clickHandle);
        $("#deny-btn").click(clickHandle);

        if (!(text === "")) {
            $("#info-box").css("width", (num + 195) + 'px');
            $("#messagebox").css("width", '190px');
            $("#info-box").css("height", '35px');
            $("#messageholder").css("width", '190px');
            $("#messageholder").css("border-right", '#000000 solid 2px');
            $("#messageholder").css("padding-right", '2px');
            $('#messagebox').click(function() {
                passMessage("fade");
            });
        } else {
            if (num == 34) num = 45;
            $("#info-box").css("width", num + 'px');
            $("#messageholder").css("display", "none");
            $("#imgs").css("margin-top", '1px');
            $("#imgs").css("float", 'none');
            $("#imgs").css("display", 'inline-block');
        }

    } else if (!(text === "")) {
        $(".bubble").css("visibility", "visible");
        setFade();
        $("#info-box").css("width", '195px');
        $("#messagebox").css("width", '190px');
        $("#messageholder").css("width", '190px');
        $("#imgs").css("display", "none");
        $("#info-box").css("height", '35px');
        $('#messagebox').click(function() {
            passMessage("fade");
        });
    } else {
        passMessage("fade");
    }
});
