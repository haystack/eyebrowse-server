"use strict";

function setFade() {

    var fadeTime = 2000; //2 seconds
    var $popup = $(".popup");

    var fadePopup = setTimeout(function() {
        fade($popup);
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
    $(".popup").remove();
    var message = {
        "action": action,
        "type": type,
    };
    window.parent.postMessage(JSON.stringify(message), "*");
}


function fade(el) {
    var $popup = $(".popup");
    el.fadeOut(1000, function() {
        $popup.animate({
            "top": $(".popup").css("top") - 120
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
    setFade();
    $("#allow-btn").click(clickHandle);
    $("#deny-btn").click(clickHandle);
});
