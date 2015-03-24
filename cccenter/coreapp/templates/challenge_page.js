<script>
    /* challenge_page.js
     *
     * This page is linked to the challenge html pages to get ciphertexts, check plaintexts,
     * and run the comments and forum sections.
     */
     
    var home_url = "http://cccenter473.appspot.com";
    //var home_url = "http://localhost:8080";

    function getCiphertext() {
        // get a ciphertext
        $.ajax({
            url: home_url + "/solve", // source page
            type: "GET",
            data: {}, // no paramaters as of yet
            dataType: 'json', // return data type
            async: true,
            success: function(data) { // what to do when the data is recieved
                // put the ciphertext on the page
                $('#ciphertextDisplay').text(data['cipher']);
            },
            error: function(){alert('fail');}
        });
    }

    function checkPlaintext() {
        // send the plaintext for verification
        var pt = $('#plaintextDisplay').text();
        
        // submit the plaintext
        $.ajax({
            url: home_url + "/solve/check", // source page
            type: "POST",
            data: JSON.stringify(pt), // no paramaters as of yet
            contentType: 'application/json', // data type sent to server
            dataType: 'application/json', // data type expected from server
            async: true,
            success: function(data) { // what to do when the data is recieved
                // put the ciphertext on the 
                alert(data); // for now
                //TODO post result to page
                
            }
        });
    }
</script>
