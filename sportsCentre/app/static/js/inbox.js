// Hide the facility field based on the position selection waits for the document to be ready before executing
$(document).ready(function() {
  $('#position').on('change', function() {
    if ($(this).val() == 'instructor') {
      $('#facility_div').show();
    } else {
      $('#facility_div').hide();
    }
  });
});
