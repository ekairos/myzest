$(document).ready(function() {

/*
                Ingredients
*/
    var ingredientCount = $(".ing-item").length;

    // Add extra ingredient form field in new recipe form
    window.addIngredient = function() {
        ingredientCount ++;
        let ingredient = '<li class="row valign-wrapper">\
                        <div class="input-field col s7">\
                            <label for="ingredient-' + ingredientCount + '">Ingredient ' + ingredientCount + '</label>\
                            <input id="ingredient-' + ingredientCount + '" class="validate" type="text" maxlength="30" name="ingredient-' + ingredientCount + '" pattern="[0-9A-Za-z()\\s]{3,30}" required>\
                            <span class="helper-text" data-error="Specify ingredient\'s name or delete"></span>\
                        </div>\
                        <div class="input-field col s4">\
                            <label for="amount-' +ingredientCount +'">Amount</label>\
                            <input id="amount-' + ingredientCount + '" class="validate" type="text" maxlength="15" name="amount-' + ingredientCount + '" pattern="[0-9A-Za-z\\s]{1,15}" required>\
                            <span class="helper-text" data-error="Specify valid amount or delete"></span>\
                        </div>\
                        <i class="material-icons cancel col s1" onclick="removeIngredient(this)">cancel</i>\
                    </li>'
        $('#ingredient-list').append(ingredient);
    }

    // When an ingredient is removed, it resets the counter
    // to update remaining ingredients names and ids

    function resetIng() {
        var ingredients = $('#ingredient-list .row');
        ingredientCount = 0;
        ingredients.each(function() {
            ingredientCount ++;
            var currentIng = "ingredient-" + ingredientCount;
            var currentQty = "amount-" + ingredientCount;
            $(this).find("[id^='ingredient']").attr("id", currentIng);
            $(this).find("[id^='ingredient']").attr("name", currentIng);
            $(this).find("[for^='ingredient']").attr("for", currentIng);
            $(this).find("[for^='ingredient']").html("Ingredient " + ingredientCount);
            $(this).find("[id^='amount']").attr("id", currentQty);
            $(this).find("[id^='amount']").attr("name", currentQty);
            $(this).find("[for^='amount']").attr("for", currentQty);
            $(this).find("[for^='amount']").html("Amount");
        });
    }

    window.removeIngredient = function(e) {
        $(e).parent().remove();
        resetIng();
    }

/*
                Steps
*/
    var stepCount = $(".step-item").length;

    // adding extra step
    window.addStep = function() {
        stepCount ++;
        let step = '<li class="row valign-wrapper">\
                    <div class="input-field col s11 mb-2 mt-2">\
                    <label for="step-' + stepCount + '">Step ' + stepCount + '</label>\
                    <textarea class="validate materialize-textarea" name="step-' + stepCount + '" required maxlength="300"></textarea>\
                    <span class="helper-text" data-error="This field is required"></span>\
                    </div class="col s1">\
                    <i class="material-icons cancel col s1" onclick="removeStep(this)">cancel</i>\
                    </li>'
        $('#step-list').append(step);
    }

    // When a step is removed, it reset the step counter
    // and updates remaining steps name and id

    function resetStep() {
        var steps = $('#step-list textarea');
        stepCount = 0;
        steps.each(function() {
            stepCount ++;
            var currentStep = "step-" + stepCount;
            $(this).attr("id", currentStep);
            $(this).attr("name", currentStep);
            $(this).prev("label").attr("for", currentStep);
            $(this).prev("label").html("Step " + stepCount);
        });
    }

    window.removeStep = function(e) {
        $(e).parent().remove();
        resetStep();
    }

/*
                Custom Validation
*/
    // Pic extension validation
    var picExtensions = ["jpeg", "jpg", "png", "gif"];
    $("#img-btn").on("blur", function() {
        var ext = $(this).val().split('.').pop();
        if (picExtensions.indexOf(ext) == -1) {
            $("#img-path").next(".helper-text").attr("data-error", "A valid file is required (jpeg, jpg, png or gif)");
            $("#img-path").removeClass("valid").addClass("invalid");
            document.getElementById("img-btn").setCustomValidity("Invalid file format");
        }
        if (picExtensions.indexOf(ext) > -1) {
            $("#img-path").removeClass("invalid").addClass("valid");
            document.getElementById("img-btn").setCustomValidity("");
        }
    })

    $("#difficulty").closest(".select-wrapper").on("change", function() {
        $(this).removeClass("invalid");
        $(this).addClass("valid");
    })

    window.validateForm = function() {
        // reset error messages
        if ($(".field-error").length) {
            $(".field-error").remove();
        }

        // Check materialize select input for required recipe's difficulty
        var diffvalid = document.getElementById("difficulty").checkValidity();
        if (diffvalid == false) {
            $("#difficulty").closest(".select-wrapper").addClass("invalid");
            let diffError = '<div class="mb-4 field-error">Please select Difficulty</div>'
            $("#submit-btn").append(diffError);
        }

        // Check file type inserted
        var imgvalid = document.getElementById("img-btn").checkValidity();
        if (imgvalid == false && $("form").attr("id") == "newRecipeForm") {
            let imgError = '<div class="mb-4 field-error">Please insert valid image file</div>'
            $("#submit-btn").append(imgError);
        } else {
            document.getElementById("img-btn").setCustomValidity("");
        }

        var formValid = document.getElementsByTagName("form")[0].checkValidity();
        if (formValid == false) {
            let formError = '<div class="mb-4 field-error">Some details are missing or not valid</div>'
            $("#submit-btn").append(formError);
        }
    }
});