$(function(){
    new liveStreamPing(getURLParameter, 'following',{'template':'history_item_template'});
    $('.history-container').on('click', '.connection', follow);
});