function setTips() {
    var $targets = $('.cut-content');
    $.each($targets, function(index, target) {
        $target = $(target)
        makeTip($target, $target.data('content'), 'right', 'hover');
    });
    
}
$(function(){
    setTips();//set tool tips for truncated data
    $('.history-data').stupidtable();
}); 