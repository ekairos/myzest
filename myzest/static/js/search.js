$(document).ready(function(){

    // Get time search values from template variables
    var timeMin = $("#timer-start").attr("data-timer-start");
    var timeMax = $("#timer-stop").attr("data-timer-stop");
    var timeRange;

    if (timeMin !== "" && timeMax !== "") {
        timeRange = [timeMin, timeMax];
    } else {
        timeRange = [$("#timer-start").attr("min"), $("#timer-stop").attr("max")];
    }

    var searchTimer = document.getElementById('search-timer');

    // Create slider for time criteria search
    noUiSlider.create(searchTimer, {
		start: timeRange,
		connect: true,
		step: 5,
		orientation: 'horizontal',
		range: {
			'min': 5,
			'max': 240
		},
		format: {
			from: function (value) {
				return Number(value.replace(',', ''));
			},
			to: function (value) {
				return Math.round(value);
			}
		}
	});

    // Get serve search values from template variables
    var serveMin = $("#serve-start").attr("data-serve-start");
    var serveMax = $("#serve-stop").attr("data-serve-stop");
    var serveRange;

    if (serveMin !== "" && serveMax !== "") {
        serveRange = [serveMin, serveMax];
    } else {
        serveRange = [$("#serve-start").attr("min"), $("#serve-stop").attr("max")];
    }

    var servings = document.getElementById('serving');

    // Create slider for serve criteria
    noUiSlider.create(servings, {
		start: serveRange,
		connect: true,
		step: 1,
		orientation: 'horizontal',
		range: {
			'min': 1,
			'max': 20
		},
		format: {
			from: function (value) {
				return Number(value.replace(',', ''));
			},
			to: function (value) {
				return Math.round(value);
			}
		}
	});

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
            "textSearch": $("#text-search").val().toLowerCase(),
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

    $("#text-search, #timer-start, #timer-stop, #serve-start, #serve-stop, #food-field, #diff-field").on("keyup blur change", function(){
        countRecipes();
    });

});
