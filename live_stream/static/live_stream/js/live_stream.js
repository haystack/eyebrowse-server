function insertHistoryItem(e, d){
    var $toAdd = $(data.commprods.shift());

    $toAdd.addClass('first');
    $toAdd.hide();
    $toAdd.css('opacity', 0);

    $(e.currentTarget).find('.first').removeClass('first');
    $(e.currentTarget).prepend($toAdd);

    $toAdd.slideDown(function(){
        $toAdd.animate({opacity:1}, 150);
    });
    if (data.commprods.length == 0) {
        $(document).trigger('complete_rec')
    }
    if (data.commprods.length < 10){
        ping();
    } 

    //add popover since this commprod wasn't arround when it was first added
    $toAdd.find('.permalink').hover(detailsCorrectionText, detailsDefaultText).popover()
    //same for favoriting
    $toAdd.find('.fav').hover(favToggle).click(favVote);
}

function ping(cb){
    $.getJSON('/live_stream/ping', {
        filter:true, 
        limit:15, 
        rec: true, 
        orderBy:'?', 
        return_type:'list'
        }, function(res){
            data.commprods = data.commprods.concat(res.res);
            if (cb){
                cb(res);
            }
    });
    $(document).trigger('requestMoreProds', {loc: 'home'});
}

$(function(){
    var $history_timeline = $('.history-timeline');

    $history_timeline.on('updateHistory', insertHistoryItem)
    

    ping(function(){
        $('.new-history').hide();
        $history_timeline.trigger('needsCommprod');    
    });
})