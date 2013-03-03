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
            fade($popup)
        }, fadeTime);
    });
}

function passMessage(action){
    return function(){
        $(".popup").remove()
        var message = {
            "type": action,
        };
        window.parent.postMessage(JSON.stringify(message), "*")
    }
}


function fade(el) {
    var $popup = $(".popup");
    el.fadeOut(1000, function() {
        $popup.animate({
            "top": $(".popup").css("top") -120
        }, 500);
    $("body").css("z-index", -1)
    });
}

$(document).ready(function(){
    setFade();
    $("#allow-btn").click(passMessage("whitelist"));
    $("#deny-btn").click(passMessage("blacklist"));
});