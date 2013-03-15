/*

container of data to be updated must have the class '.live-stream-container'

filterFunc is a function that takes one argument, the string "filter" and returns the type of filter to apply.

defaultFilter is a string of the default filter to apply

searchParams is a dictionary of additional search params to ping the server with

updateTemplate is a html string to show when new data is available. Defaults to history container code

*/
function liveStreamPing(filterFunc, defaultFilter, searchParams, updateTemplate){
    this.history = [];
    this.canPing = true;
    this.$container = $('.live-stream-container');
    this.pingIntervalValue = 2500;
    this.searchParams = searchParams;
    this.updateTemplate = updateTemplate || "<div class='load-new pointer history-container row well'> <span class='center'> <strong> Load new items </strong> </span> </div>";

    this.setup = function() {
        this.pingInterval = setInterval($.proxy(this.ping, this), this.pingIntervalValue);
        this.setupIdle();
        this.first();
        
        //lets display results automatically
        // $(document).on('ping-new', $.proxy(this.showNotification, this));
        // this.$container.on('click', '.load-new', $.proxy(this.insertHistoryItems, this));

        $(document).on('ping-new', $.proxy(this.insertHistoryItems, this));
    }

    this.setupIdle = function() {
        var that = this;
        $(window).idle(
            function() {
                that.canPing = false; // cheap insurance
                clearInterval(that.pingInterval);
            },
            function() {
                that.canPing = true;
                that.pingInterval = setInterval($.proxy(that.ping, that), that.pingIntervalValue);
            }
        );
    }

    this.ping = function(callback){
        if (!this.canPing) return;
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
        console.log("pingload", payload)
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
        $('.empty-search').remove();
        $('.first').removeClass('first');
        var $loadNew = $('.load-new');
        $loadNew.fadeOut();
        var that = this;
        $.each(that.history.reverse(), function(index, item){
            var $toAdd = $(item);
            $toAdd.hide();
            that.$container.prepend($toAdd);

            $toAdd.fadeIn(750);
            if (index === that.history.length -1){
                $toAdd.addClass('first');
            }
        });

        this.history = [];
        $loadNew.remove();
    }

    if (ping !== undefined && ping === true){
        this.setup()    
    }
    return this
}