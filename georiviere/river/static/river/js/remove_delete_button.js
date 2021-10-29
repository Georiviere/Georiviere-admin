$(document).ready(function() {
    $('.form-actions a.delete').attr('href', '#')

    $('.form-actions a.delete').attr('class', 'btn disabled delete')

    $('.form-actions a.delete').attr('title', gettext("You can't delete this !"))
});
