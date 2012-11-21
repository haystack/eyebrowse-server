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
    //var username = user_dict[val];
    //window.location = '/users/' + username
}

function submitForm(e, d){
    e.preventDefault();
    var $form = $(e.target);
    var id = $form.attr('id');
    var url = $form.data('url');
    $form.find('.btn[type=submit]').button('loading')
    $form.find('.alert').slideUp();
    
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

///////// templating helpers /////

/*
template_list is a list of elments initially sent by the server
renderFunc is what these items are sent into
*/
function setupTemplateValues(template_list, renderFunc, type) {
    if (template_list != undefined) { 
        $.each(template_list, function(index, item){
            item = {
                'success': true,
                'data': item,
            }
            renderFunc(item, type);
        });
    }
}

/*
Adds a new row or creates an intial row the given type of row to add 
*/
function initTemplateTable(type) {
    var $rows = $(sprintf('.%s-row', type));
    var $toAdd, addFunc;
    if ($rows.length == 0 ){
        $toAdd = $(sprintf('.%s-body', type))
        addFunc = 'append';
    } else {
        $toAdd = $rows.filter(':last');
        addFunc = 'after'
    }
    return {
        'toAdd' : $toAdd,
        'addFunc' : addFunc,
    }
}

/*
Given a rendered template appends it to the proper row given by init template table
*/
function addTableTemplate(type, template) {
    var init = initTemplateTable(type);
    var $toAdd = init.toAdd;
    var addFunc = init.addFunc;
    $toAdd[addFunc](template);
}

//defaults to placing right and focus trigger if 
//no values given.
function makeTip(selector, title, placement, trigger) {
    placement = placement || 'right';
    trigger = trigger || 'focus'
    $(selector).tooltip({
        "placement" : placement,
        "title" : title,
        "trigger" : trigger,
    });
}

//helper function for fomatting numbers with commas
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function getApiURL(resource, id, params) { 
    params = params || {};
    var apiBase = '/api/v1/' + resource;
    var getParams = '';
    $.each(params, function(key, val){
        getParams += sprintf("&%s=%s", key, val);
    });
    if (id != null) {
        apiBase += '/' + id;
    } 
    return sprintf("%s?format=json%s", apiBase, getParams)
}

/*
Deletes a resource, requires data of resource type and the id of the item to be in the item triggering the event.
*/
function rmItem(e) {
    var $target = $(e.currentTarget);
    var id = $target.data('id');
    $target.closest('tr').remove()
    $.ajax({
        url: getApiURL(e.data, id),
        type: 'DELETE',
    });
}

/*
Deletes a resource, requires data of resource type and the id of the item to be in the item triggering the event.
*/
function addItem(resource, url) {
    $.ajax({
        type: 'POST',
        url: getApiURL(resource),
        data:  JSON.stringify({ "url" : url, "user" : getResourceURI()}),
        contentType:'application/json',
        dataType: 'application/json',
        processData: false,
    });
}

function follow(e) {
    var $icon = $(e.currentTarget).children();
    var type = $icon.data('type');
    $.post('/accounts/connect', $icon.data(), function(res){
        if(res.success){
            swapFollowClass($icon, type);
        }
    });
}

function swapFollowClass(icon, type) {
    console.log(arguments)
    var $icon = $(icon);
    if (type == 'add-follow'){
        $icon.attr('data-type', 'rm-follow');
        $icon.removeClass('icon-ok').addClass('icon-remove');
        var text = $icon.parent().html().replace('Follow', 'Following')
        $icon.parent().html(text);
        ;
    } else {
        $icon.attr('data-type', 'add-follow');
        $icon.removeClass('icon-remove').addClass('icon-ok');
        var text = $icon.parent().html().replace('Following', 'Follow')
        $icon.parent().html(text);
    }
}

function getResourceURI() { 
    return sprintf('/api/v1/user/%s/', username)
}


function urlDomain(url, cut) {
    cut = cut || true;
    var uri = new URI(url)
    var hostname = uri.hostname();
    if (cut) {
        hostname = truncate(hostname);
    }
    return hostname
}

function truncate(str, len){
    len = len || 40;
    return str.substr(0, len);
}

function date_ms(dateString) {
    dateString = dateString.replace('a.m.', 'AM').replace('p.m.', 'PM');
    return (new moment(dateString).unix())*1000
}

$(function(){
    TEMPLATE_BASE = "api/js_templates/";
    $(document).on('click', '#submit_feedback', submitFeedBack)

    $(document).on('typeaheadItemSelected', dropitemSelected)

    $('#search_bar').typeahead({
        'source' : []
    });
}); 