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
    if (res.success) {
        $('.rm-margin').val('')
        var $rows = $(sprintf('.%s-row', type));
        var $toAdd, addFunc;
        if ($rows.length == 0 ){
            $toAdd = $(sprintf('.%s-body', type))
            addFunc = 'append';
        } else {
            $toAdd = $rows.filter(':last');
            addFunc = 'after'
        }
        var template = ich['api/js_templates/filterset_row.html']({
                'url' : res.data.url,
                'id' : res.data.id,
                'type' : type,
            });

        $toAdd[addFunc](template);
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
        $('.filter-input').val('').trigger('keyup');

    }
    
}

function handleFormResponse(e, d){
    return addFilterlist(d, d.type)
}

function setupFilterList() {
    if (whitelist_filterset != undefined) { 
        $.each(whitelist_filterset, function(index, item){
            item = {
                'success':true,
                'data': item,
            }
            addFilterlist(item, 'whitelist');
        });
    }
}


// custom css expression for a case-insensitive contains()
$.expr[':'].Contains = function(a,i,m){
  return (a.textContent || a.innerText || "").toUpperCase().indexOf(m[3].toUpperCase())>=0;
};


function listFilter(list) {

    $('.filter-input').change(function() {
        var filter = $(this).val();
        if(filter) {
          // this finds all links in a list that contain the input,
          // and hide the ones not containing the input while showing the ones that do
          $(list).find("a:not(:Contains(" + filter + "))").closest('tr').slideUp();
          $(list).find("a:Contains(" + filter + ")").closest('tr').slideDown();
        } else {
          $(list).find("tr").slideDown();
        }
        $('.rm-whitelist').click('whitelist', rmFilterListItem);
        return false;
      })
    .keyup( function () {
        // fire the above change event after every letter
        $(this).change();
    });
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

    setupFilterList();
    listFilter($(".whitelist-body"));
});
