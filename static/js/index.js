$(function() {
    $('button').click(function() {
        var ID = $('#inputTwitterID').val();
        $.ajax({
            url: '/process',
            data: {},
            type: 'POST'
        }).done(function(data) {
            $('#close_ids').text(data.close_ids).show();
            $('#far_ids').text(data.far_ids).show();
        });
    })
})