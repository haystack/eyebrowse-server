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
    setTips('.cut-content');//set tool tips for truncated data
    addHeadButtonListener()
    var updateTemplate = "<tr class='load-new pointer history-row'><td class='load-new-background' colspan='4'><strong>Load new content.</strong></td>"
    new liveStreamPing(nullFilter, 'none', {
        'username' : $('.user-info').data('username'),
        'template' : 'history_row',
        }, updateTemplate);
    $('.history-body').on('click', '.rm-history', 'history-data', rmEyeHistoryItem);
}); 