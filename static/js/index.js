$(function() {
    $('#close_id_card').hide();
    $('#far_id_card').hide();

    let both = false;
    let select = document.getElementById('social');
    select.addEventListener('change', e => {
        if (e.target.value === 'both') {
            $("#inputID").attr("placeholder", "Your Reddit ID");
            $('#idForm').append('<input type="text" id="inputID2" name="ID" class="col form-control" placeholder="Your Twitter ID" required/>')
            both = true;
        } else if (e.target.value === 'twitter') {
            $("#inputID").attr("placeholder", "Your Twitter ID");
            let ID2el = document.getElementById('inputID2');
            if (ID2el) {
                ID2el.remove();
            }
        } else {
            $("#inputID").attr("placeholder", "Your Reddit ID");
            let ID2el = document.getElementById('inputID2');
            if (ID2el) {
                ID2el.remove();
            }
        }
    })

    $('form').on("submit", function(e) {
        const ID = $('#inputID').val();
        let ID2;
        if(both) {
            ID2 = $('#inputID2').val();
        }

        if (ID) {
            const social = $('#social').val();
            const consent = $('#consent').prop('checked');
            let senddata;
            switch (social) {
                case "twitter":
                    senddata = {'consent': consent, 'social':social, 'ID':ID};
                    break;
                case "reddit":
                    senddata = {'consent': consent, 'social':social, 'ID':ID};
                    break;
            }

            $.ajax({
                url: '/process',
                data: senddata,
                type: 'POST'
            }).done(function (data) {
                $('#close_id_card').show();
                $('#far_id_card').show();
                $('#close_ids').empty();
                $('#far_ids').empty();

                data.close_ids.forEach(ID => {
                    let p = document.createElement("p");
                    p.textContent = JSON.stringify(ID);
                    $('#close_ids').append(p);
                })

                data.far_ids.forEach(ID => {
                    let p = document.createElement("p");
                    p.textContent = JSON.stringify(ID);
                    $('#far_ids').append(p);
                })
            }).fail(function (err) {
                alert(err);
            })
        }
        e.preventDefault();
    })
})
