$(document).ready(function() {

    // Fav Button
	window.favMe = function() {
		if (typeof sessionUsr != 'undefined') {
            $.ajax({
                contentType: "application/json; charset=utf-8",
                data : JSON.stringify({
                    "recipe_id": recipe_id,
                    "user_id": sessionUsr._id
                }),
                method : "POST",
                url : "/favme"
            })
            .done(function(response){
                if (response.message == "removed") {
                    $("#favme .material-icons").html("favorite_border");
                    $("#favme").attr("data-tooltip", "Add to favs");
                } else if (response.message == "added") {
                    $("#favme .material-icons").html("favorite");
                    $("#favme").attr("data-tooltip", "Remove from favorites");
                }
            });
		}
	}

    // Fav icon
	if (sessionUsr == "") {
    	$("#favme").attr("data-tooltip", "Login to add as favorite");
	    $("#favme").attr("href", "/login");
	} else if (sessionUsr.username == author) {
	    console.log("sessionUsr name is same as author ie:", sessionUsr.username);
        $("#favme").attr("data-tooltip", "This recipe is yours");
    } else if (sessionUsr.hasOwnProperty('favorites') && sessionUsr.favorites.includes(recipe_id)) {
        $("#favme .material-icons").html("favorite");
        $("#favme").attr("data-tooltip", "Remove from favorites");
	} else {
	    $("#favme").attr("data-tooltip", "Add as favorite");
	}

});