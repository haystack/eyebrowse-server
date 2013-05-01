$(function(){

    //set tool tips for truncated data
    setTips('.cut-content'); 

    new liveStreamPing({
        'filterFunc' : nullFilter,
        'defaultFilter' : 'none', 
        'searchParams' : {
            'template':'history_row',
            'username' : $('.user-info').data('username'),
            'orderBy': 'end_time', 
            'direction': 'hl',
            'filter' : '',
        },
    }, updateStats);
}); 