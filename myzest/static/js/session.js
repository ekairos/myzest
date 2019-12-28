$(document).ready(function() {

    var authorName = $("#rcp-author").attr("data-author-name");
    var recipeId = $("#rcp-name").attr("data-recipe-id");
    var sessionUser = JSON.parse($("#sessionUserData").attr("data-user-id"));

    // Fav Button
	window.favMe = function() {
		if (typeof sessionUser !== 'undefined' && sessionUser.username !== authorName) {
            $.ajax({
                contentType: "application/json; charset=utf-8",
                data : JSON.stringify({
                    "recipe_id": recipeId,
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
    } else if (sessionUser.hasOwnProperty('favorites') && sessionUser.favorites.includes(recipeId)) {
        $("#favme .material-icons").html("favorite");
        $("#favme").attr("data-tooltip", "Remove from favorites");
	} else {
	    $("#favme").attr("data-tooltip", "Add as favorite");
	}

});