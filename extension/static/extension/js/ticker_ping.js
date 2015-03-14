"use strict";

/*

container of data to be updated must have the class ".ticker-stream-container"

defaultFilter is a string of the default filter to apply

updateTemplate is a html string to show when new data is available. Defaults to history container code

*/
function TickerPing(args, callback) {
    this.history = [];
    this.canPing = true;
    this.$container = $(".ticker-stream-container");
    this.pingIntervalValue = 10000;
    this.defaultFilter = args.defaultFilter;
    this.searchParams = args.searchParams;
    this.updateTemplate = args.updateTemplate || "<div class='load-new pointer history-container row well'> <span class='center'> <strong> Load new items </strong> </span> </div>";
    this.callback = callback;
    this.historyQueue = [];

    this.setup = function() {
        var curTime = new Date();
        this.lastTime = curTime.format("yyyy-mm-dd HH:MM:ss");
        // this.lastTime = curTime.getFullYear()+"-"+curTime.getMonth()+"-"+curTime.getDate()+" "+curTime.getHours()+":"+curTime.getMinutes()+":"+curTime.getSeconds();

        this.pingInterval = setInterval($.proxy(this.ping, this), this.pingIntervalValue);
        // this.setupIdle();
        this.first();

        setInterval($.proxy(this.dequeue, this), 3000);

        //lets display results automatically instead
        // $(document).on("ping-new", $.proxy(this.showNotification, this));
        // this.$container.on("click", ".load-new", $.proxy(this.insertHistoryItems, this));

        $(document).on("ping-new", $.proxy(this.insertHistoryItems, this));
    };

    this.ping = function() {
        if (!this.canPing) {
            return;
        }
        var filter = this.defaultFilter;

        var timestamp = this.lastTime /*"2014-10-31 19:10:20"*/ ;
        // console.log(timestamp);
        var curTime = new Date();
        this.lastTime = curTime.format("yyyy-mm-dd HH:MM:ss");
        var payload = {
            "filter": filter,
            "timestamp": timestamp,
            "return_type": "list",
            "type": "ping",
        };
        for (var attrname in this.searchParams) {
            payload[attrname] = this.searchParams[attrname];
        }
        var that = this;
        $.getJSON("/live_stream/ping/", payload, function(res) {
            // console.log("res", res);
            that.history = res.history;
            if (that.callback) {
                that.callback(res);
            }
            if (that.history.length) {
                // console.log("that.history:", that.history);
                $(document).trigger("ping-new");
            }
        });
    };

    this.first = function() {
        this.$container.children().first().addClass("first");
    };

    this.showNotification = function() {
        if (!$(".load-new").length) {
            this.$container.prepend(this.updateTemplate);
        }
    };

    this.insertHistoryItems = function(e) {
        var that = this;
        $.each(that.history.reverse(), function(index, item) {
            that.historyQueue.push(item);
        });
        this.historyQueue = that.historyQueue;
        this.history = [];
    };

    this.dequeue = function() {
        var that = this;
        if (that.historyQueue.length > 0) {
            $(".bubble").css("visibility", "visible");
            that.$container.empty();
            var $toAdd = $(that.historyQueue.shift());
            $toAdd.hide();
            $toAdd.fadeIn(750);
            that.$container.prepend($toAdd);
        } else {
            $(".bubble").css("visibility", "hidden");
        }
        this.historyQueue = that.historyQueue;
    };

    this.setup();
    return this;
}
