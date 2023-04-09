// get the value of the country field and store it in a variable
let countrySelected = $('#id_default_country').val();
// fist option = empty string so can be used as boolean
if(!countrySelected) {
    $('#id_default_country').css('color', '#aab7c4');
};
// capture change event
$('#id_default_country').change(function() {
    // get value every time box changes
    countrySelected = $(this).val();
    // determine the proper colour
    if(!countrySelected) {
        // grey if it is not selected
        $(this).css('color', '#aab7c4');
    } else {
        // black if it is
        $(this).css('color', '#000');
    }
});