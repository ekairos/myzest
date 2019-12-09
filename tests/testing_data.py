from bson.objectid import ObjectId

fake_user_entry = {
    "username": "john",
    "email": "John@gmail.com",
    "password": "1234",
    "favorites": [],
    "avatar": "default.png"
}

fake_author = {
    "_id": ObjectId("5ddee60b8e1daf2ccbebb81c"),
    "username": "George",
    "email": "george@gmail.com",
    "password": "1234",
    "recipes": ["ObjectId('5ddee63cae10027121293947')"],
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
    'views': 0,
    'image': 'none.jpg',
    'updated': '2019-08-20'}
