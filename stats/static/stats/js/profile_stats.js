//humanize the timestamps passed down
function calculateStats() {
    $.each($(".time-stat"), function(i, v){
        v = $(v);
        v.text(moment.humanizeDuration(v.data('time')));
    });
}

$(function(){
    calculateStats();
    makeTip(".fav-site", $(".fav-site").data("content"), "top", "hover");
}); 