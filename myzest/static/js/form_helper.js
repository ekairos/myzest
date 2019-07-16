$(document).ready(function(){
	$("#email").on("focusout", function() {
	    // sets default error message
		$("#email_help").attr("data-error", "invalid entry");
		if ($("#email").val() != "" && $("#email").hasClass("valid")) {
			$.ajax({
				contentType: "application/json; charset=utf-8",
				data : JSON.stringify({
					"email": $(this).val(),
					"form": $("form").attr("id")
				}),
				method : "POST",
				url : "/check_usr",
			})
			.done(function(response){
				console.log(response);
				if (response.error) {
					$("#email_help").attr("data-error", response.message);
					$("#email").removeClass("valid");
					$("#email").addClass("invalid");
				}
				if (response == "success") {
				    $("#email").removeClass("invalid");
				    $("#email").addClass("valid");
				}
			})
		}
	});
	$("#username").on("blur", function() {
		if ($("#username").val() != "") {
			$.ajax({
				contentType: "application/json; charset=utf-8",
				data : JSON.stringify({
					"username": $(this).val()
				}),
				method : "POST",
				url : "/check_usr",
			})
			.done(function(response){
				console.dir(response);
				if (response.error) {
					$("#username_help").attr("data-error", response.message);
					$("#username").removeClass("valid");
					$("#username").addClass("invalid");
				}			
			});
		}
	});
	$("[type=password]").on("blur", function() {
		if ($("#password").val() != "" && $("#passwConfirm").val() != "" && $("#passwConfirm").length != 0) {
			if ($("#passwConfirm").val() != $("#password").val()) {
				$("[type=password]").addClass("invalid");
				$("[type=password]").next("span").attr("data-error", "Passwords do not match");
			} else {
				$("[type=password]").removeClass("invalid");
			}
		}
	});
	$("[required]").on("focusout", function() {
        if ($(this).val() == '') {
            $(this).next("span").attr("data-error", "This field is required")
        }
    });
});