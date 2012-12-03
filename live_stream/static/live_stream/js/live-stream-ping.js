/*

container of data to be updated must have the class '.live-stream-container'

filterFunc is a function that takes one argument, the string "filter" and returns the type of filter to apply.

defaultFilter is a string of the default filter to apply

searchParams is a dictionary of additional search params to ping the server with

updateTemplate is a html string to show when new data is available. Defaults to history container code

*/
function liveStreamPing(filterFunc, defaultFilter, searchParams, updateTemplate){
    this.history = [];
    this.$container = $('.live-stream-container');
    this.pingIntervalValue = 2500;
    this.searchParams = searchParams
    this.updateTemplate = updateTemplate || "<div class='load-new pointer history-container row well' style='background-color:#5bb75b !important;'> <span class='center'> <strong> Load new items </strong> </span> </div>"

    this.setup = function() {
        this.pingInterval = setInterval($.proxy(this.ping, this), this.pingIntervalValue);
        this.setupIdle();
        this.first();
        
        $(document).on('ping-new', $.proxy(this.showNotification, this));
        this.$container.on('click', '.load-new', $.proxy(this.insertHistoryItems, this));
    }

    this.setupIdle = function() {
        var that = this;
        $(window).idle(
            function() {
                clearInterval(that.pingInterval);
            },
            function() {
                that.pingInterval = setInterval($.proxy(that.ping, that), that.pingIntervalValue);
            }
        );
    }

    this.ping = function(callback){
        var filter = filterFunc('filter') || defaultFilter;
        var timestamp = $('.first .date').data('timestamp');
        var payload =  {
            'filter' : filter, 
            'timestamp' : timestamp,
            'return_type' : 'list',
            'type' : 'ping',
            }
        for (var attrname in this.searchParams) { 
            payload[attrname] = this.searchParams[attrname]; 
        }
        var that = this;
        $.getJSON('/live_stream/ping/', payload, function(res){
                that.history = res.history;
                if (callback){
                    callback(res);
                }
                if (that.history.length) {
                    $(document).trigger('ping-new');
                }     
        });
    }

    this.first = function() {
        this.$container.children().first().addClass('first');
    }

    this.showNotification = function() {
        if (!$('.load-new').length){
            this.$container.prepend(this.updateTemplate);
        }
    }

    this.insertHistoryItems = function (e){
        $('.first').removeClass('first');
        var $loadNew = $('.load-new')
        $loadNew.fadeOut();
        var that = this;
        $.each(that.history.reverse(), function(index, item){
            var $toAdd = $(item);

            $toAdd.hide();
            $toAdd.css('opacity', 0);

            that.$container.prepend($toAdd);

            $toAdd.slideDown(function(){
                $toAdd.animate({opacity:1}, 150);
            });
            if (index == that.history.length -1){
                $toAdd.addClass('first');
            }
        })

        this.history = [];
        $loadNew.remove();
    }
    this.setup()
    return this
}