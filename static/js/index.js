$(function() {
    $('#close_id_card').hide();
    $('#far_id_card').hide();

    let both = false;
    let select = document.getElementById('social');
    select.addEventListener('change', e => {
        if (e.target.value === 'both') {
            $('#idForm').append('<input type="text" id="inputID2" name="ID" class="col form-control" placeholder="Your ID" required/>')
            both = true;
        } else {
            let ID2el = document.getElementById('inputID2');
            ID2el.parentNode.removeChild(ID2el); // Such a weird wat of doing it but it works
        }
    })

    $('form').on("submit", function(e) {
        const ID = $('#inputID').val();
        if(both) {
            const ID2 = $('#inputID2').val();
        }

        if (ID) {
            const social = $('#social').val();
            const consent = $('#consent').prop('checked');
            let senddata;
            switch (social) {
                case "twitter":
                    senddata = {'consent': consent, 'twitter': ID};
                    break;
                case "reddit":
                    senddata = {'consent': consent, 'reddit': ID};
                    break;
                case "both":
                    senddata = {'consent': consent, 'reddit':ID, 'twitter':ID2}
                default:
                    senddata = {'consent': consent};
            }

            $.ajax({
                url: '/process',
                data: senddata,
                type: 'POST'
            }).done(function (data) {
                $('#close_id_card').show();
                $('#far_id_card').show();

                data.close_ids.forEach(ID => {
                    let p = document.createElement("div");
                    let attr = document.createAttribute("class");
                    attr.value = "new";
                    p.textContent = ID;
                    p.setAttributeNode(attr);
                    $('#close_ids').append(p);
                })

                data.far_ids.forEach(ID => {
                    let p = document.createElement("div");
                    let attr = document.createAttribute("class");
                    attr.value = "new";
                    p.textContent = ID;
                    p.setAttributeNode(attr);
                    $('#far_ids').append(p);
                })
            })
        }
        e.preventDefault();
    })
})