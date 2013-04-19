function addHeadButtonListener() {
    var $btn = $('.btn-prof-header');
    var $icon = $btn.children();
    var func = follow;
    $btn.click(func)
}

$(function(){
    setTips('.cut-content');//set tool tips for truncated data
    addHeadButtonListener()
    var updateTemplate = "<tr class='load-new pointer history-row'><td class='load-new-background' colspan='4'><strong>Load new content.</strong></td>"
    new liveStreamPing({
        'filterFunc' : nullFilter, 
        'defaultFilter' : 'none', 
        'searchParams' : {
            'username' : $('.user-info').data('username'),
            'template' : 'history_row',
            }, 
        'updateTempalte' : updateTemplate
    });
}); 