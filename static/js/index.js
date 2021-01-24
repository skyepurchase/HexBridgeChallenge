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

    $('form').submit(function(e) {
        e.preventDefault();

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

                data.close_ids.forEach(post => {
                    let card = document.createElement("div");
                    let cl1 = document.createAttribute("class");
                    cl1.value = "card bg-success";
                    card.setAttributeNode(cl1);

                    let header = document.createElement("div");
                    let cl2 = document.createAttribute("class");
                    cl2.value = "card-header d-flex justify-content-center";
                    header.setAttributeNode(cl2);
                    header.textContent = post.ID;

                    let body = document.createElement("div");
                    let cl3 = document.createAttribute("class");
                    cl3.value = "card-body d-flex justify-content-center";
                    body.setAttributeNode(cl3);

                    let quote = document.createElement("blockquote");
                    let cl4 = document.createAttribute("class");
                    cl4.value = post.social;
                    quote.setAttributeNode(cl4);

                    let link = document.createElement("a");
                    let href = document.createAttribute("href");
                    href.value = post.link;
                    link.setAttributeNode(href);

                    quote.append(link)
                    body.append(quote)

                    let p = document.createElement("p");
                    p.textContent = post.link;
                    body.append(p);

                    card.append(header);
                    card.append(body);
                    $('#close_ids').append(card);
                })

                data.far_ids.forEach(post => {
                    let card = document.createElement("div");
                    let cl1 = document.createAttribute("class");
                    cl1.value = "card bg-danger";
                    card.setAttributeNode(cl1);

                    let header = document.createElement("div");
                    let cl2 = document.createAttribute("class");
                    cl2.value = "card-header d-flex justify-content-center";
                    header.setAttributeNode(cl2);
                    header.textContent = post.ID;

                    let body = document.createElement("div");
                    let cl3 = document.createAttribute("class");
                    cl3.value = "card-body d-flex justify-content-center";
                    body.setAttributeNode(cl3);

                    let quote = document.createElement("blockquote");
                    let cl4 = document.createAttribute("class");
                    cl4.value = post.social;
                    quote.setAttributeNode(cl4);

                    let link = document.createElement("a");
                    let href = document.createAttribute("href");
                    href.value = post.link;
                    link.setAttributeNode(href);

                    quote.append(link)
                    body.append(quote)

                    let p = document.createElement("p");
                    p.textContent = post.link;
                    body.append(p);

                    card.append(header);
                    card.append(body);
                    $('#far_ids').append(card);
                })

            }).fail(function (data, textStatus, xhr) {
                alert("ERROR: " + data.status);
                alert("STATUS: "+xhr);
            })
        }
    })
})
