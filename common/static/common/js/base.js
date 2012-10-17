function submitFeedBack(e, d) {
    $('#submit_success').fadeIn();
    $.post('/feedback', { 
        'feedback' : $('#feedback').val()
    });
    $('#submit_success').fadeOut();
    $('#send-feedback-modal').modal('hide');
    $('#feedback').val("");
}


function dropitemSelected (e, v) {
    $('#search-bar').blur();
    //navToUser(v);
}

function navToUser(val){
    var username = user_dict[val];
    window.location = '/users/' + username
}

$(function(){
    $(document).on('click', '#submit_feedback', submitFeedBack)

    $(document).on('typeaheadItemSelected', dropitemSelected)

    $('#search_bar').typeahead({
        'source' : []
    });
}); 