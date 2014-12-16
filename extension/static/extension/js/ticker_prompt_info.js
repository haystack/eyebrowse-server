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
  var text = $.trim($("#message").text());
  $('.bubble').click(function(){
    passMessage("fade");
  });
});

function tickerCallback(history_stream) {
  console.log("history_stream", history_stream)
}

$(function(){
    tickerStream = new tickerPing({
        'defaultFilter' : 'firehose', //FOR TESTING- for deploy switch to following
        'searchParams' : {
            'template':'../extension/ticker_history_item',
            'query' :  "",
            'date' :  ""
        },
    }, tickerCallback);

    // $('.history-container').on('click', '.connection', follow);

});
