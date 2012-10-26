function removeInput(e, d){
    $(e.target).closest('p').remove();
}

function addEmailInput(){
    var template = '<p><input type="email" class="removable_input" placeholder="Alternate email" name="email"><a class="btn remove-input remove-shirt-name"><i class="icon-minus"></i></a></p>'
    $('#add-email').closest('p').before(template);
}

function switchTab(e, d) {
    $('.tab').closest('li').removeClass("active");
    $(e.target).closest('li').addClass("active");
    var id = $(e.currentTarget).attr('id').split("-")[0];
    $('.edit').addClass('hidden');
    $('#' + id).removeClass('hidden');
    $('.edit').find('.alert').slideUp(0)
}

function rmWhitelist(e, d) {
    var postUrl = '/api/whitelist/rm';
    var $target = $(e.target);
    var url = $target.data('url');
    var csrftoken = $.cookie('csrftoken')
    $target.closest('tr').remove()
    $.post(url, {
        'url': url,
        'csrftoken' : csrftoken,
    });
}

$(function(){
    $('.tab').click(switchTab);;

    $('.edit').submit(submitForm);

    $('.rm-whitelist').click(rmWhitelist);

    $(document).on('click', '.remove-input', removeInput);

    $(document).on('click', '#add-email', addEmailInput);
    
    $('#add-email').click();
    $('#whitelist-tab').click();


});
