/* challenge_page.js
 *
 * This page is linked to the challenge html pages to get ciphertexts, check plaintexts,
 * and run the comments and forum sections.
 */
 
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCiphertext() {
    // get a ciphertext
    $.ajax({
        url: "/cccenter/getcipher/", // source page relative to the current page (cccenter/)
        type: "GET",
        data: {}, // no paramaters as of yet
        dataType: 'json', // return data type
        async: true,
        success: function(data) { // what to do when the data is recieved
            // put the ciphertext on the page
            $('#ciphertextDisplay').text(data);
        },
        error: function(){alert('fail');}
    });
}

function checkPlaintext(challenge_id) {
    // send the plaintext for verification
    var pt = $('#plaintextDisplay').val();
    var csrftoken = $.cookie('csrftoken');
    
    //var csrftoken = $("[name='csrfmiddlewaretoken']");
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    
    $.ajax({
        url: "/cipher/checkplaintext/", // source page relative to the current page (cccenter/)
        type: "POST",
        data: {'challenge_id':challenge_id, 'guessed_plaintext':pt},//, 'csrfmiddlewaretoken':csrftoken}),
        //contentType: 'application/json', // data type sent to server
        //dataType: 'application/json', // data type expected from server
        async: true,
        success: function(data) { // what to do when the data is recieved
            // put the ciphertext on the 
            if (data['success'] == true) {
                //alert('You got it!');
                //window.location.reload(true);
                $('#alert-failure').hide();
                $('#alert-success').show();
            }
            
            else {
                //alert('Not quite...');
                $('#alert-failure').show();
                $('#alert-success').hide();
            }
            //TODO post result to page
            
        }
    });
}

function joinChallenge(challenge_id) {
    var csrftoken = $.cookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    
    $.ajax({
        url: "/cipher/joinchallenge/",
        type: "POST",
        data: {'challenge_id':challenge_id},
        //contentType: 'application/json',
        async: false,
        success: function(data) {
            window.location.reload(true);
        }
    });
}
