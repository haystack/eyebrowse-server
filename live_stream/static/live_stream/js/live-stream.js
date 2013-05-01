$(function(){
    new liveStreamPing({
        'filterFunc' : getURLParameter,
        'defaultFilter' : 'following', 
        'searchParams' : {'template':'history_item_template_new'},
    }, updateStats);
    $('.history-container').on('click', '.connection', follow);
});