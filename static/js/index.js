$(function() {
    $('#close_ids').hide();
    $('#far_ids').hide();
    $('button').click(function() {
        var ID = $('#inputTwitterID').val();
        var social = $('#social').val();
        $.ajax({
            url: '/process',
            data: {social: ID},
            type: 'POST'
        }).done(function(data) {
            $('#close_ids').show();
            $('#far_ids').show();
            $('#close_id').text(data.close_ids).show();
            $('#far_id').text(data.far_ids).show();
        });
    });
})