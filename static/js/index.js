$(function() {
    $('#close_id_card').hide();
    $('#far_id_card').hide();
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

        $('#close_id_card').show();
        ['Hello', 'World', 'Classic', 'Programming', 'Test'].forEach(ID => {
            let p = document.createElement("p")
            p.textContent = ID;
            $('#close_ids').append(p);
        })
        $.ajax({
            url: '/process',
            data: senddata,
            type: 'POST'
        }).done(function(data) {
            $('#close_id_card').show();
            $('#far_id_card').show();

            data.close_ids.forEach(ID => {
                let p = document.createElement("p")
                p.textContent = ID;
                $('#close_ids').append(p);
            })

            data.far_ids.forEach(ID => {
                let p = document.createElement("p")
                p.textContent = ID;
                $('#far_ids').append(p);
            })
        });
    });
})