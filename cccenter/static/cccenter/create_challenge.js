 // The function prevents a user from choosing difficulty if a cipher is selected.
 // Similarly if a difficulty is selected it prevents the user from selecting a cipher.
 $('body').click(function() 
 {
    // Check if the click was a difficulty choice
    // If it is checked, then disable a cipher choice and make it blank
    if(event.target.id == "createSubmit")
    {
        return;
    }
    if(event.target.id == "difficultyRadio")
    {
        if ($(event.target).is(":checked")) 
        {
          $("#cipherChoice").prop("disabled", true);
          $('select').val('0');
        } 
    }
    // Check if the click was a cipher choice
    // If an option is selected disable the difficulty choice
    else if(event.target.id == "cipherChoice")
    {   
        if ($( "select option:selected" ))
        { 
            $('input[type="radio"]').prop('disabled', true); 
        } 
    }
    // Else a click was made on the body
    // Uncheck the radio buttons, make the radio buttons clickable, and allow selection of a cipher
    else 
    {
        $('input[type="radio"]').prop('checked', false);
        $('input[type="radio"]').prop('disabled', false);  
        $("#cipherChoice").prop("disabled", false); 
    }
 });