
// Goolgle login
function signInCallback(authResult) {
    if (authResult['code']) {
        // Hide the sign-in button now that the user is authorized
        $('#signinButton').attr('disabled', 'disabled');

        // Send the one-time-use code to the server, if the server responds, write a 'login successful' message to the web page and then redirect back to the main catalogs page
        $.ajax({
            type: 'POST',
            url: '/gconnect?state=' + state,
            processData: false,
            data: authResult['code'],
            contentType: 'application/octet-stream; charset=utf-8',
            success: function (result) {
                // Handle or verify the server response if necessary.
                console.log('Login complete');
                gapi.load('auth2', function () {
                    gapi.auth2.init();
                    console.log(gapi.auth2, '....');
                });
                if (result) {
                    window.location.href = "/";
                }
                console.log('Whatagwayn')
            }
        });
    }
}
