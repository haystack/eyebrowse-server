$(function(){
    calculateStats();
    makeTip(".fav-site", $(".fav-site").data("content"), "left", "hover");
    $('.btn-prof-header').click(follow);
}); 