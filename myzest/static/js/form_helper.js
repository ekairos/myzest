$(document).ready(function(){

    function checkInput(field, form) {
    	if (field.hasClass("valid")) {
			$.ajax({
				contentType: "application/json; charset=utf-8",
				data : JSON.stringify({
					"field": field.attr("id"),
					"value": field.val(),
					"form": form
				}),
				method : "POST",
				url : "/check_user"
			})
			.done(function(response){
				if (response.error) {
					field.next(".helper-text").attr("data-error", response.error);
					field.removeClass("valid").addClass("invalid");
				}
				if (response === "success") {
				    field.removeClass("invalid").addClass("valid");
				}
			});
		}
	}

	window.clearField = function(e) {
        $(e).parent().find("textarea", "input").val('');
    };

	$("[required]").on("focusout", function() {
        if ($(this).val() === '') {
            $(this).next("span").attr("data-error", "This field is required")
        }
    });

	$("#email").on("blur", function() {
		if ($(this).val() !== "" && $(this).hasClass("invalid")) {
			$(this).next('.helper-text').attr("data-error", "Invalid email format");
		} else if ($(this).val() !== "" && $(this).parents("form").attr("id") !== "contact-form") {
            checkInput($(this), $(this).parents("form").attr("id"));
		}
	});

	$("#username").on("blur", function() {
		checkInput($(this), $(this).parents("form").attr("id"));
	});

	$("[type=password]").on("blur", function() {
		if ($("#password").val() !== "" && $("#passwConfirm").val() !== "" && $("#passwConfirm").length !== 0) {
			if ($("#passwConfirm").val() !== $("#password").val()) {
				$("[type=password]").addClass("invalid");
				$("[type=password]").next("span").attr("data-error", "Passwords do not match");
			} else {
				$("[type=password]").removeClass("invalid");
			}
		}
	});
});