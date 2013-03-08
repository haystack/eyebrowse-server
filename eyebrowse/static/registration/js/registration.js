/* 
    Function for modifying styles on registration related pages.
*/

function set_title(title) {
    var base_title = "eyebrowse";
}

function login() {
    $('#id_username').attr('placeholder', 'Username or Email');
    $('#id_password').attr('placeholder', 'Password');}

function register() {
    $('#id_username').attr('placeholder', 'Username');
    $('#id_email').attr('placeholder', 'Email');
    $('#id_password1').attr('placeholder', 'Password');
    $('#id_password2').attr('placeholder', 'Password (again)');
    $('th').remove()
}

function change_password() {
    $('#id_old_password').attr('placeholder', 'Old Password');
    $('#id_new_password1').attr('placeholder', 'New Password');
    $('#id_new_password2').attr('placeholder', 'New Password (again)');
    $('th').remove()
}

$(document).ready(function() {
    login()
    register()
    change_password()
});