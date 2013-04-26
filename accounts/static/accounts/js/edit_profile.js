function removeInput(e, d){
    $(e.target).closest('p').remove();
}

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
        return false;
      })
    .keyup( function () {
        // fire the above change event after every letter
        $(this).change();
    });
}


function checkboxValue(e){
    $target = $(e.target);
    if (e.target.checked) {
        $target.val('True')
    } else {
        $target.val('False')
    }
}

$(function(){

    $('.alert').hide();
    $('.edit').submit(submitForm);
    
    //account info
    $("#account-info").on('click', '.checkbox', checkboxValue);
    $('#upload').click(getImg);
    setTips('.tip');

    //following tab
    $('#following').on('click', '.connection', follow)
    listFilter($(".following-body"));

    //followers tab
    $('#followers').on('click', '.connection', follow)
    listFilter($(".followers-body"));

});