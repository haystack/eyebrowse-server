function addHeadButtonListener() {
    var $btn = $('.btn-prof-header');
    var $icon = $btn.children();
    var func = follow;
    $btn.click(func)
}

$(function(){
    addHeadButtonListener();
}); 