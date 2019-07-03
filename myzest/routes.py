from flask import render_template
from myzest import app, mongo
from bson.objectid import ObjectId


@app.route('/')
@app.route('/home')
def home():
    recipes = mongo.db.recipes.find()
    return render_template('home.html', recipes=recipes)


@app.route('/recipe/<recipe_id>')
def get_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('recipe.html', recipe=recipe)
