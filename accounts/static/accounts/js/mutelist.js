function setupFilterList() {
    setupTemplateValues(mutelist_filterset, addFilterlist, 'mutelist')
    setupTemplateValues(mutelist_filterset_word, addFilterlist2, 'mutelist')
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
        var data = res.data;
        data.type = type;
    	if ($('.add-word').val() != '') {
    		var template = ich[TEMPLATE_BASE + 'mutelist_set_row2.html'](data);
    		$('.add-word').val('')
    	} else {
    		var template = ich[TEMPLATE_BASE + 'mutelist_set_row.html'](data);
    		$('.add-url').val('')
    	}
    }
    addTableTemplate(type, template)
}

function addFilterlist2(res, type){
    if (res.success && type == 'mutelist') {
        $('.add-url').val('')
        $('.add-word').val('')
        var data = res.data;
        data.type = type;
        var template = ich[TEMPLATE_BASE + 'mutelist_set_row2.html'](data);
    }
    addTableTemplate(type, template)
}

function rmFilterListItem(e) {
    var $target = $(e.currentTarget);
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