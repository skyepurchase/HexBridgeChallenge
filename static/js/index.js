$(function() {
    $('#close_id_card').hide();
    $('#far_id_card').hide();
    $('form').on("submit", function(e) {
        const ID = $('#inputID').val();

        if (ID) {
            const social = $('#social').val();
            const consent = $('#consent').prop('checked');
            let senddata;
            switch (social) {
                case "twitter":
                    senddata = {'consent': consent, 'IDs':{'twitter': ID}};
                    break;
                case "reddit":
                    senddata = {'consent': consent, 'IDs':{'reddit': ID}};
                    break;
                default:
                    senddata = {'consent': consent, 'IDs':{}};
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