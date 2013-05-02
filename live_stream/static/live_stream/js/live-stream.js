function submitSearch(e) {
    if (e.which !== 1 && e.which !== 13) return
    var query = $(".search-bar").val();
    var date = $(".date-search-bar").val();
    var filter = getURLParameter("filter");
    var url = sprintf("/live_stream/?query=%s&date=%s&filter=%s", query, date, filter);
    document.location = url;
}

$(function(){
    new liveStreamPing({
        'filterFunc' : getURLParameter,
        'defaultFilter' : 'following', 
        'searchParams' : {
            'template':'history_item_template_new'
        },
    }, liveStreamCallback);

    calculateStats();

    makeTip(".date-search-bar", "Limit search by date.", "bottom", "hover");

    $('.history-container').on('click', '.connection', follow);
    $('.search-btn').click(submitSearch);
    $('.date-search-bar').keypress(submitSearch);
    $('.search-bar').keypress(submitSearch);
});