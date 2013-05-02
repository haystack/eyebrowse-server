$(function(){

    //set tool tips for truncated data
    setTips('.cut-content'); 

    liveStream = new liveStreamPing({
        'filterFunc' : nullFilter,
        'defaultFilter' : 'none', 
        'searchParams' : {
            'template':'history_item_template_new',
            'username' : profile_username,
            'orderBy': 'end_time', 
            'direction': 'hl',
            'filter' : '',
            'query' :  $(".search-bar").val(),
            'date' :  $(".date-search-bar").val(),
        },
    }, updateStats);
});