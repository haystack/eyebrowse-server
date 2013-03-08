function setFade() {
    
    var fadeTime = 2000; //2 seconds
    var $popup = $(".popup");
    
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

function passMessage(action){
    $(".popup").remove();
    var message = {
        "type": action,
    };
    window.parent.postMessage(JSON.stringify(message), "*")
}


function fade(el) {
    var $popup = $(".popup");
    el.fadeOut(1000, function() {
        $popup.animate({
            "top": $(".popup").css("top") -120
        }, 500);
        passMessage("remove");
    });
}

$(document).ready(function(){
    setFade();
    $("#allow-btn").click(function(){passMessage("whitelist")});
    $("#deny-btn").click(function(){passMessage("blacklist")});
});