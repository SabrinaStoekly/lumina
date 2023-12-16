// Function to update the text color of the default country field
function updateCountryFieldColor() {
    let countrySelected = $('#id_default_country').val();
  
    // Check if a country is selected
    if (!countrySelected) {
      // If no country is selected, change the text color to light grey
      $('#id_default_country').css('color', '#ECE8DF');
    } else {
      // If a country is selected, change the text color to black
      $('#id_default_country').css('color', '#000');
    }
  }
  
  // Call the function initially when the page loads
  $(document).ready(function() {
    updateCountryFieldColor(); // Set the initial color based on the selected value
  
    // Listen for changes in the selected country
    $('#id_default_country').change(function() {
      // Update the text color whenever the selection changes
      updateCountryFieldColor();
    });
  });