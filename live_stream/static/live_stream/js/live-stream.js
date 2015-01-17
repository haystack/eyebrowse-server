$(function(){
    liveStream = new liveStreamPing({
        'filterFunc' : getURLParameter,
        'defaultFilter' : 'following',
        'searchParams' : {
            'template':'history_item_template_new',
            'query' :  $(".search-bar").val(),
            'date' :  $(".date-search-bar").val(),
        },
    }, liveStreamCallback);

    calculateStats();

    $('.history-container').on('click', '.connection', follow);

});