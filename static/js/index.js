$(function() {
    $('#close_ids').hide();
    $('#far_ids').hide();
    $('button').click(function() {
        const ID = $('#inputTwitterID').val();
        const social = $('#social').val();
        const consent = $('#consentYes').prop('checked');
        let senddata;
        switch (social) {
            case "twitter":
                senddata = {'consent': consent, 'twitter': ID};
                break;
            case "reddit":
                senddata = {'consent': consent, 'reddit': ID};
                break;
            default:
                senddata = {'consent': consent};
        }
        $.ajax({
            url: '/process',
            data: senddata,
            type: 'POST'
        }).done(function(data) {
            $('#close_ids').show();
            $('#far_ids').show();
            $('#close_id').text(data.close_ids).show();
            $('#far_id').text(data.far_ids).show();
        });
    });
})