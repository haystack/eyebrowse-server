//humanize the timestamps passed down
function calculateStats() {
    $.each($(".time-stat"), function(i, v){
        v = $(v);
        v.text(moment.humanizeDuration(v.data('time')));
    });
}

$(function(){
    
    calculateStats();
    makeTip(".fav-site", $(".fav-site").data("content"), "left", "hover");
    $('.btn-prof-header').click(follow);
}); 