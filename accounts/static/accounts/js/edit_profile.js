function removeInput(e, d){
    $(e.target).closest('p').remove();
}

function addEmailInput(){
    var template = '<p><input type="email" class="rm-margin" placeholder="Alternate email" name="email"><a class="btn remove-input"><i class="icon-minus"></i></a></p>'
    $('#add-email').closest('p').before(template);
}

function switchTab(e) {
    $('.tab').closest('li').removeClass("active");
    $(e.target).closest('li').addClass("active");
    var id = $(e.currentTarget).attr('id').split("-")[0];
    $('.edit').addClass('hidden');
    $('#' + id).removeClass('hidden');
    $('.edit').find('.alert').slideUp(0)
}

function rmWhitelistItem(e) {
    var $target = $(e.target);
    var id = $target.data('id');
    $target.closest('tr').remove()
    $.ajax({
        url: getApiURL('whitelist', id),
        type: 'DELETE',
    });

}

function addWhitelist(res){
    console.log(res.data.id)
    if (res.success) {
        $('.rm-margin').val('')
        var $rows = $('.whitelist-row');
        var $toAdd;
        if ($rows.length == 0 ){
            $toAdd = $('.whitelist-body')
        } else {
            $toAdd = $rows.filter(':last');
        }
        var template = ich['api/js_templates/whitelist_row.html']({
                'url' : res.data.url,
                'id' : res.data.id,
            });

        $toAdd.after(template);
        $('.rm-whitelist').click(rmWhitelistItem);

    }
}

function handleFormResponse(e, d){
    if (d.type == 'whitelist') {
        addWhitelist(d)
    }
}


$(function(){
    $('.tab').click(switchTab);;

    $('.edit').submit(submitForm);

    $('.edit').on('formRes', handleFormResponse);

    $('.rm-whitelist').click(rmWhitelistItem);

    $(document).on('click', '.remove-input', removeInput);

    $(document).on('click', '#add-email', addEmailInput);
    
    $('#add-email').click();
    $('#whitelist-tab').click();

});
