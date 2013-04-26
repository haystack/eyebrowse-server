function updateStats(history_data) {
    $("#tot_history .content").html(numberWithCommas(history_data.num_history));
    $("#tot_online .content").html(numberWithCommas(history_data.num_online));
}

$(function(){
    new liveStreamPing({
        'filterFunc' : getURLParameter,
        'defaultFilter' : 'following', 
        'searchParams' : {'template':'history_item_template_new'},
    }, updateStats);
    $('.history-container').on('click', '.connection', follow);
});