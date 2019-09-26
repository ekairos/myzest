$(document).ready(function(){

    // Init search sidenav and prevent swipe sliders interactions
    $('#slide-search').sidenav({"draggable": false});

    // Link input fields and sliders values
    searchTimer.noUiSlider.on('update', function(values, handle) {
        if (handle) {
            $("#timer-stop").val(values[handle]);
        } else {
            $("#timer-start").val(values[handle]);
        }
    });
    searchTimer.noUiSlider.on('end', function() {
        countRecipes();
    });
    $("#timer-start").on("change", function() {
        searchTimer.noUiSlider.set([$(this).val(), null]);
    });
    $("#timer-stop").on("change", function() {
        searchTimer.noUiSlider.set([null, $(this).val()]);
    });

    servings.noUiSlider.on('update', function(values, handle) {
        if (handle) {
            $("#serve-stop").val(values[handle]);
        } else {
            $("#serve-start").val(values[handle]);
        }
    });
    servings.noUiSlider.on('end', function() {
        countRecipes();
    });
    $("#serve-start").on("update", function() {
        servings.noUiSlider.set([$(this).val(), null]);
    });
    $("#serve-stop").on("change", function() {
        servings.noUiSlider.set([null, $(this).val()]);
    });

    // Count recipes to return
    function countRecipes() {
        var formdata = {
            "textSearch": $("#text-field").val().toLowerCase(),
            "foodType": $("#food-field .selected").text().toLowerCase(),
            "difficulty": $("#diff-field .selected").text().toLowerCase(),
            "timer.start": parseInt($("#timer-start").val()),
            "timer.stop": parseInt($("#timer-stop").val()),
            "serve.start": parseInt($("#serve-start").val()),
            "serve.stop": parseInt($("#serve-stop").val())
        };
        $.ajax({
            contentType: "application/json; charset=utf-8",
            method: 'post',
            url: '/searchcount',
            data: JSON.stringify(formdata)
        })
        .done(function(response){
            $("#recipe-count").text(response.nbr_recipes + " recipes matching");
        });
    }

    $("input, #food-field, #diff-field").on("keyup blur change", function(){
        countRecipes();
    });

});
