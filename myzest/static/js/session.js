$(document).ready(function() {

    // Fav Button
	window.favMe = function() {
		if (typeof sessionUser !== 'undefined' && sessionUser.username !== authorname) {
            $.ajax({
                contentType: "application/json; charset=utf-8",
                data : JSON.stringify({
                    "recipe_id": recipe_id,
                    "user_id": sessionUser._id
                }),
                method : "POST",
                url : "/favme"
            })
            .done(function(response){
                if (response.message === "removed") {
                    $("#favme .material-icons").html("favorite_border");
                    $("#favme").attr("data-tooltip", "Add to favs");
                } else if (response.message === "added") {
                    $("#favme .material-icons").html("favorite");
                    $("#favme").attr("data-tooltip", "Remove from favorites");
                }
            });
		}
	};

    // Fav icon
	if (sessionUser === "") {
    	$("#favme").attr("data-tooltip", "Login to add as favorite");
	    $("#favme").attr("href", "/login");
	} else if (sessionUser.username === authorname) {
        $("#favme").attr("data-tooltip", "This recipe is yours");
    } else if (sessionUser.hasOwnProperty('favorites') && sessionUser.favorites.includes(recipe_id)) {
        $("#favme .material-icons").html("favorite");
        $("#favme").attr("data-tooltip", "Remove from favorites");
	} else {
	    $("#favme").attr("data-tooltip", "Add as favorite");
	}

});