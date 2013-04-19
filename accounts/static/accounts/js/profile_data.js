$(function(){

    //set tool tips for truncated data
    setTips('.cut-content'); 

    var updateTemplate = "<tr class='load-new pointer history-row'><td class='load-new-background' colspan='4'><strong>Load new content.</strong></td>";

    new liveStreamPing({
        'filterFunc' : nullFilter, 
        'defaultFilter' : 'none', 
        'searchParams' : {
            'username' : $('.user-info').data('username'),
            'template' : 'history_row',
            }, 
        'updateTempalte' : updateTemplate,
    });
}); 