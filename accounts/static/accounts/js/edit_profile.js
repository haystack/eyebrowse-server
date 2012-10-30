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

function addFilterlist(res, type){
    console.log()
    if (res.success) {
        $('.rm-margin').val('')
        var $rows = $(sprintf('.%s-row', type));
        var $toAdd;
        if ($rows.length == 0 ){
            $toAdd = $(sprintf('.%s-body', type))
        } else {
            $toAdd = $rows.filter(':last');
        }
        var template = ich[sprintf('api/js_templates/%s_row.html', type)]({
                'url' : res.data.url,
                'id' : res.data.id,
            });

        $toAdd.after(template);
        $('.rm-whitelist').click('whitelist', rmFilterListItem);
        $('.rm-blacklist').click('blacklist', rmFilterListItem);

    }
}

function rmFilterListItem(e) {
    var $target = $(e.target);
    var id = $target.data('id');
    if (!isNaN(id)){
        $target.closest('tr').remove()
        $.ajax({
            url: getApiURL(e.data, id),
            type: 'DELETE',
        });
    }
    
}

function handleFormResponse(e, d){
    return addFilterlist(d, d.type)
}


$(function(){
    $('.tab').click(switchTab);;

    $('.edit').submit(submitForm);

    $('.edit').on('formRes', handleFormResponse);

    $('.rm-whitelist').click('whitelist', rmFilterListItem);
    $('.rm-blacklist').click('blacklist', rmFilterListItem);

    $(document).on('click', '.remove-input', removeInput);

    $(document).on('click', '#add-email', addEmailInput);
    
    $('#add-email').click();
    $('#whitelist-tab').click();

});
