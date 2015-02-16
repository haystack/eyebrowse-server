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
    
    $('#tagModal').on('show.bs.modal', function (event) {
	  var button = $(event.relatedTarget) // Button that triggered the modal
	  var recipient = button.data('domain') // Extract info from data-* attributes
	  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
	  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
	  var modal = $(this)
	  modal.find('.modal-title').text('New message to ' + recipient)
	  modal.find('.modal-body input').val(recipient)
	})

});