function setupFilterList() {
    setupTemplateValues(mutelist_filterset, addFilterlist, 'mutelist')
}

// custom css expression for a case-insensitive contains()
$.expr[':'].Contains = function(a,i,m){
  return (a.textContent || a.innerText || "").toUpperCase().indexOf(m[3].toUpperCase())>=0;
};

function handleFormResponse(e, d){
    return addFilterlist(d, d.type)
}

function addFilterlist(res, type){
    if (res.success && type == 'mutelist') {
        $('.add-url').val('')
        var data = res.data;
        data.type = type;
        var template = ich[TEMPLATE_BASE + 'filterset_row.html'](data);
    }
    addTableTemplate(type, template)
}

function rmFilterListItem(e) {
    var $target = $(e.currentTarget);
    var url = $target.data('url');
    if (rmItem(e, "mutelist")) {    
        $('.filter-input').val('').trigger('keyup');
    }
}

$(function(){
    $('.edit').on('formRes', handleFormResponse);

    //whitelist
    $(".mutelist").on("click", ".rm-mutelist", rmFilterListItem);

    setupFilterList();
    listFilter($(".mutelist-body"));

});