function setTips() {
    var $targets = $('.cut-content');
    $.each($targets, function(index, target) {
        $target = $(target);
        makeTip($target, $target.data('content'), 'right', 'hover');
    });
    
}

function rmEyeHistoryItem(e) {
    rmItem(e);
}

function toggleHistory(e) {
    $('.edit').fadeToggle().toggleClass('hidden');
}

$(function(){
    setTips();//set tool tips for truncated data
    $('.history-data').stupidtable();
    $('table').on('click', '.rm-history', 'history-data', rmEyeHistoryItem);
    $('.btn-rm-history').click(toggleHistory)
}); 