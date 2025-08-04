// Check the initial value of the country dropdown 
let countrySelected = $('#id_default_country').val();
if(!countrySelected) {
    $('#id_default_country').css('color', '#aab7c4');
};

/**
 * Event listener for the Country dropdown's change event.
 * Updates the text color based on whether a country is selected.
 */
$('#id_default_country').change(function() {
    countrySelected = $(this).val();
    if(!countrySelected) {
        $(this).css('color', '#aab7c4');
    } else {
        $(this).css('color', '#000');
    }
});