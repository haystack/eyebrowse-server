function insertHistoryItems(e){
    $('.first').removeClass('first');
    $('.load-new').fadeOut();
    $.each(data.history.reverse(), function(index, item){
        var $toAdd = $(item);

        $toAdd.hide();
        $toAdd.css('opacity', 0);

        $('.history-timeline-container').prepend($toAdd);

        $toAdd.slideDown(function(){
            $toAdd.animate({opacity:1}, 150);
        });
        if (index == data.history.length){
            $toAdd.addClass('first');
        }
    })

    data.history = []
}

function ping(callback){
    var filter = getURLParameter('filter') || 'following';
    if (filter == 'null'){
        filter = 'following'
    }
    var timestamp = $('.first .date').data('timestamp');
    $.getJSON('/live_stream/ping/', {
        'filter' : filter, 
        'timestamp' : timestamp,
        'return_type' : 'list',
        'type' : 'ping',
        }, function(res){
            data.history = res.history;
            if (callback){
                callback(res);
            }
            if (data.history.length) {
                $(document).trigger('ping-new');
            }     
    });
}

function addFirst() {
    $('.history-timeline-container').children().first().addClass('first');
}

function showNewHistoryNotification() {
    var newHistoryTemplate = "<div class='load-new pointer history-container row well'> <span class='center'> <strong> Load new items </strong> </span> </div>"
    if (!$('.load-new').length){
        $('.history-timeline-container').prepend(newHistoryTemplate);
    }
}

function setupIdle(){
    /*
        https://github.com/jasonmcleod/jquery.idle
        Detect if the current tab is idle or not and close/open the active item respectively. 
    */
    $(window).idle(
        function() {
            clearInterval(pingInterval);
        },
        function() {
            setInterval(ping, 2500);
        },  
        {
            'after': 5000, //5s idle
        });
}

$(function(){
    setupIdle();
    addFirst();
    data = {
        'history' : []
    }
    
    $('.history-timeline-container').on('click', '.load-new', insertHistoryItems);
    $(document).on('ping-new', showNewHistoryNotification);
    
    pingInterval = setInterval(ping, 2500);
})