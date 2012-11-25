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

function rmEyeHistoryItem(e) {
    rmItem(e);
}

function toggleHistory(e) {
    $('.edit').fadeToggle().toggleClass('hidden');
}

function addHeadButtonListener() {
    var $btn = $('.btn-prof-header');
    var $icon = $btn.children();
    var func = follow;
    if ($icon.hasClass('edit-history')) {
        func = toggleHistory;
    }
    $btn.click(func)
}

$(function(){
    setupHistoryList();
    setTips('.cut-content');//set tool tips for truncated data
    addHeadButtonListener()
    $('.history-data').stupidtable();
    $('.history-body').on('click', '.rm-history', 'history-data', rmEyeHistoryItem);
}); 