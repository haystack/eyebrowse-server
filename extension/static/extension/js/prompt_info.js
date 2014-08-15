function setFade() {
    
    var fadeTime = 4000; //8 seconds
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

function passMessage(action, type){
    $("#info-box").remove();
    var message = {
        "action" : action,
        "type": type,
    };
    window.parent.postMessage(JSON.stringify(message), "*")
}


function fade(el) {
    var $popup = $(".popup");
    el.fadeOut(1000, function() {
        $popup.animate({
            "top": $("#info-box").css("top") -120
        }, 500);
        passMessage("fade");
    });
}

function clickHandle(e){
    var action = $(e.target).data("action");
    var type = $(e.target).data("type");
    passMessage(action, type);
    passMessage("fade"); //remove iframe on btn click
}

$(document).ready(function(){
	var num_img = $("#info-box img").length;
	if (num_img > 0) {
		$(".bubble").css("visibility", "visible");
	    setFade();
	    var num = (num_img * 24) + 10;
	    $("#info-box").css("width", num + 'px');
	    $("#allow-btn").click(clickHandle);
	    $("#deny-btn").click(clickHandle);
	} else {
		passMessage("fade");
	}
});