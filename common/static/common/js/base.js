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
    navToUser(v);
}

function navToUser(val){
    var username = user_dict[val];
    window.location = '/users/' + username
}

function submitForm(e, d){
    e.preventDefault();
    var $form = $(e.target);
    var id = $form.attr('id');
    var url = $form.data('url');
    $form.find('.btn[type=submit]').button('loading')
    $.post(url, $form.serialize(), function(res){
        if (res.success){
            var addClass = "alert-success";
            var removeClass = "alert-error";
            var text = '<p>' + res.success + '</p>';
        } else {
            var addClass = "alert-error";
            var removeClass = "alert-success";
            var text = "";
            for (var i =0, max=res.errors[id].length; i<max; i++){
                text += "<p>" + res.errors[id][i] + "</p>";
            }
        }
        $form.find('.response_text').html(text)
        $form.find('.alert').removeClass(removeClass).addClass(addClass).slideDown();
        $form.find('.btn[type=submit]').button('reset')

        $('#pic').find('.btn[type=submit]').addClass('disabled')//reset pic submit to be disabled.
        $form.trigger('formRes', res)
    });
}

//defaults to placing right and focus trigger if 
//no values given.
function makeTip(div, title, placement, trigger) {
    placement = placement || 'right';
    trigger = trigger || 'focus'
    $('#' + div).tooltip({
        "placement" : placement,
        "title" : title,
        "trigger" : trigger,
    });
}

//helper function for fomatting numbers with commas
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function renderHistoryRow(historyData) {
    var $history_row = ich['api/jstemplates/row_history.html'](
        {
            'title' : historyData.title,
            'start_time' : historyData.start_time,
            'end_time' : historyData.end_time,
            'total_time' : historyData.total_time,
        });
}

function renderWhitelistRow(whitelist) {
    var $history_row = ich['api/jstemplates/row_history.html'](
        {
            'title' : historyData.title,
            'start_time' : historyData.start_time,
            'end_time' : historyData.end_time,
            'total_time' : historyData.total_time,
        });
}


$(function(){
    $(document).on('click', '#submit_feedback', submitFeedBack)

    $(document).on('typeaheadItemSelected', dropitemSelected)

    $('#search_bar').typeahead({
        'source' : []
    });
}); 