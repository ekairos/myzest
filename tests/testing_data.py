from bson.objectid import ObjectId

fake_user_entry = {
    "username": "john",
    "email": "John@gmail.com",
    "password": "1234",
    "favorites": [],
    "avatar": "default.png"
}

fake_user = {
    '_id': ObjectId("5dc3e2b72aa378780b20ad26"),
    "username": "Lily",
    "email": "lili@gmail.com",
    "password": "1234",
    "recipes": [],
    "favorites": [],
    "avatar": "default.png"
}

fake_author = {
    "_id": ObjectId("5ddee60b8e1daf2ccbebb81c"),
    "username": "George",
    "email": "george@gmail.com",
    "password": "1234",
    "recipes": [ObjectId('5ddee63cae10027121293947')],
    "favorites": [],
    "avatar": "default.png"
}

fake_recipe = {
    '_id': ObjectId("5ddee63cae10027121293947"),
    'name': 'Salmon Nigiri Sushi',
    'author_id': ObjectId("5ddee60b8e1daf2ccbebb81c"),
    'difficulty': 'hard', 'foodType': 'main',
    'ingredients': [
        {'name': 'salmon', 'amount': '160g'},
        {'name': 'rice', 'amount': '320g'},
        {'name': 'nori seaweed', 'amount': '5'},
        {'name': 'salt', 'amount': '5g'},
        {'name': 'soy sauce', 'amount': '5ml'},
        {'name': 'sushi vinegar', 'amount': '80ml'}],
    'time': {'total': '120'},
    'serves': '2',
    'steps': [
        {'description': 'Clean the rice in fresh water and leave it to dry in a strainer for about 20min.'},
        {'description': "Spread the freshly cooked sushi rice and pour over the sushi vinegar. Mix them with a 'cutting motion' until the rice begins to be sticky."},
        {'description': 'Slice the salmon into desired thickness, about 3mm.'},
        {'description': 'Place the desired amount of sushi rice in your hand and gently squeeze it into an easy-to-eat shape.'},
        {'description': 'Place the salmon slice on top and gently press the Nigiri into shape.'},
        {'description': 'Repeat the last 2 steps until you run out of rice or salmon.'}],
    'views': 1,
    'image': 'none.jpg',
    'updated': '2019-08-20'}

chocolate_recipe_entry = {
    "name": "Chocolate Brownie",
    "description": "Easy dark chocolate brownie with peanuts",
    "difficulty": "easy",
    "time": 50,
    "serves": 8,
    "ingredient-1": "dark bitter chocolate",
    "amount-1": "300g",
    "ingredient-2": "butter",
    "amount-2": "100g",
    "ingredient-3": "white sugar",
    "amount-3": "1 cup",
    "ingredient-4": "eggs",
    "amount-4": "5",
    "ingredient-5": "cocoa powder",
    "amount-5": "3/4 cup",
    "ingredient-6": "flour",
    "amount-6": "1 cup",
    "image": "5d63e6ae096eed71a1b73d49.jpg",
    "step-1": "Preheat oven to 180C. Line a 20 x 30 cm slice tin or brownie pan.",
    "step-2": "Sift the flour and cocoa. Melt the butter and chocolate in a bowl over a saucepan of simmering water. Stir until melted then remove from the heat.",
    "step-3": "Beat the eggs and sugar until pale and thick. Add the chocolate and mix until combined.",
    "step-4": "Beat the sieved flour mixture into the chocolate. The mixture will be quite thick. Add chopped peanuts.",
    "step-5": "Pour into the pan and bake for approximately 30 minutes. The brownie needs to be just cooked.",
    "step-6": "The brownie needs to be just cooked. Test with a skewer: it is ready when there are some crumbs still attached to the skewer.",
    "step-7": "Leave to cool a little before cutting and serving.",
    "foodType": "dessert"
}
