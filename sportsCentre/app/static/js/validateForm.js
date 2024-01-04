// This function is used to validate if the password and fields match.
// If they do not match, an alert will be shown and the function will return false.
function validate() {
    var pass = document.getElementById("password").value;
    var cpass = document.getElementById("cpassword").value;
    if (pass == cpass) {
        return true;
    } else {
        alert("Passwords do not match");
        return false;
    }
}


