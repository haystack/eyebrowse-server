"use strict";

function setupFilterList() {
    setupTemplateValues(whitelist_filterset, addFilterlist, 'whitelist')
}

// custom css expression for a case-insensitive contains()
$.expr[':'].Contains = function(a, i, m) {
    return (a.textContent || a.innerText || "").toUpperCase().indexOf(m[3].toUpperCase()) >= 0;
};

function handleFormResponse(e, d) {
    return addFilterlist(d, d.type)
}

function addFilterlist(res, type) {
    if (res.success && type == 'whitelist') {
        $('.add-url').val('');
        var data = res.data;
        data.type = type;
        var template = ich[TEMPLATE_BASE + 'filterset_row.html'](data);
    }
    addTableTemplate(type, template);
}

function rmFilterListItem(e) {
    var $target = $(e.currentTarget);
    var url = $target.data('url');
    addItem('blacklist', url);
    if (rmItem(e, "whitelist")) {
        $('.filter-input').val('').trigger('keyup');
    }
}

$(function() {
    $('.edit').on('formRes', handleFormResponse);

    //whitelist
    $(".whitelist").on("click", ".rm-whitelist", rmFilterListItem);

    setupFilterList();
    listFilter($(".whitelist-body"));
});
