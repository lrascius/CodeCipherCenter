 $('body').click(function() 
 {
    if(event.target.id == "difficultyRadio")
    {
		if ($(event.target).is(":checked")) 
    	{
          $("#cipherChoice").prop("disabled", true);
          $('select').val('0');
        } 
        else 
        {
           $("#cipherChoice").prop("disabled", false);  
        }
 	}
    else if(event.target.id == "cipherChoice")
    {	
    	if ($( "select option:selected" ))
    	{ 
 			$('input[type="radio"]').prop('disabled', true); 
        } 
        else 
        {
           $("#cipherChoice").prop("disabled", false);  
        }
    }
 	else
 	{
 		$('input[type="radio"]').prop('checked', false);
 		$('input[type="radio"]').prop('disabled', false);  
 		$("#cipherChoice").prop("disabled", false); 
 	}
 });
