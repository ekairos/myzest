$(document).ready(function () {
    $("#contact-form").submit(function(e){
        e.preventDefault();
    });

    $("textarea#message").characterCounter();

    // Init materializecss modal
    $(".modal").modal();
    var modal = M.Modal.getInstance($("#confirmation"));

    var fakesend = function() {

        // reset error messages
        if ($(".field-error").length) {
            $(".field-error").remove();
        }

        var emailValid = document.getElementById("email").checkValidity();
        var messageValid = document.getElementById("message").checkValidity();
        var nameInvalid = $("#username").hasClass("invalid");
        if (emailValid === false || messageValid === false || nameInvalid === true) {
            let formError = '<div class="mb-4 field-error">Some details are missing or not valid</div>';
            $("#submit-btn").after(formError);
        } else {
            modal.open();
        }
    };

    $("button").on("click", function () {
        // awaits ajax '/check_usr'
        setTimeout(fakesend, 250);
    });
});