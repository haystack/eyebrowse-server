function setupHistoryList() {
    setupTemplateValues(eye_history, addHistoryList, 'history')
}

function addHistoryList(res, type) {
    if (res.success) {
        var data = getData(res);
        var template = ich[TEMPLATE_BASE + 'row_history.html'](data);
    }
    addTableTemplate(type, template)
}

function getData(res) {
    var data = res.data;
    data.urlDomain = urlDomain(data.url);
    data.truncateTitle = truncate(data.title);
    data.start_time_ms = date_ms(data.start_time);
    data.end_time_ms = date_ms(data.end_time);
    return data
}

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
    setupHistoryList();
    setTips();//set tool tips for truncated data
    $('.history-data').stupidtable();
    $('.history-body').on('click', '.rm-history', 'history-data', rmEyeHistoryItem);
    $('.btn-rm-history').click(toggleHistory)
}); 