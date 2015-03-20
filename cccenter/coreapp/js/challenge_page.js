/* challenge_page.js
 *
 * This page is linked to the challenge html pages to get ciphertexts, check plaintexts,
 * and run the comments and forum sections.
 */

function getCipherText() {
    // add jQuery to the page (in case it's not already there)
    /*var jqscript = document.createElement('script');
    jqscript.src = '/js/jquery-2.1.3.min.js';
    jqscript.type = 'text/javascript';
    document.getElementsByTagName('head')[0].appendChild(jqscript);*/
    
    // get a ciphertext
    $.get(
        "", // source page
        {}, // no parameters as of yet
        function(data) { // what to do when the data is recieved
            // put the ciphertext on the page
            $('#ciphertextDisplay').text(data)
        }
    )
}

function checkPlainText() {
    // send the plaintext for verification
    
}
