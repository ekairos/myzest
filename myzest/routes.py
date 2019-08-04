from flask import render_template, request, jsonify, redirect, flash, session
from myzest import app, mongo, bcrypt
from bson.objectid import ObjectId
import re
from datetime import date
from os import path


rcp_diff = ("easy", "average", "hard")
rcp_foodTypes = mongo.db.foodtype.distinct("name")
rcp_foodTypes.sort()
rcp_foodCategories = mongo.db.category.distinct("name")
rcp_foodCategories.sort()

pic_extensions = ("jpg", "jpeg", "png", "gif")


@app.route('/')
@app.route('/home')
def home():
    recipes = mongo.db.recipes.find()
    return render_template('home.html', recipes=recipes)


@app.route('/recipe/<recipe_id>')
def get_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('recipe.html', recipe=recipe)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        flash('{}, you are already logged in'.format(session['user']['name']), 'info')
        return redirect('home')
    return render_template('register.html')


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    data = request.form.to_dict()
    hashed_passw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = {
        'username': data['username'].title(),
        'email': data['email'].lower(),
        'password': hashed_passw
    }
    user_in_db = mongo.db.users.find_one({"$or": [{"username": new_user["username"]}, {"email": new_user["email"]}]})
    if user_in_db:
        flash('This user already exists', 'warning')
    elif user_in_db is None:
        registered_user = mongo.db.users.insert_one(new_user)
        session['user'] = {'name': new_user['username'], 'id': str(registered_user.inserted_id)}
        flash('Welcome {} ! Your account was created with {}'
              .format(new_user['username'], new_user['email']), 'success')
    return redirect('home')


@app.route('/check_usr', methods=['POST'])
def check_usr():
    data = request.get_json()
    if data['field'] == 'username':
        if mongo.db.users.find_one({'username': data['userdata'].title()}):
            return jsonify({'error': 'username', 'message': 'This username is already taken'})
    if data['field'] == 'email':
        email = mongo.db.users.find_one({'email': data['userdata'].lower()})
        if data['form'] == "registration" and email is not None:
            return jsonify({'error': 'email', 'message': 'This email is already in use'})
        if data['form'] == "login" and email is None:
            return jsonify({'error': 'email', 'message': 'This email is not registered'})
    return 'success'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        flash('{}, you are already logged in'.format(session['user']['name']), 'info')
        return redirect('home')
    return render_template('login.html')


@app.route('/log_usr', methods=['GET', 'POST'])
def log_usr():
    data = request.form.to_dict()
    user = mongo.db.users.find_one({'email': data['email']})
    if user and bcrypt.check_password_hash(user['password'], data['password']):
        flash('Welcome back {} !'.format(user['username']), 'success')
        session['user'] = {'name': user['username'], 'id': str(user['_id'])}
        return redirect('home')
    elif user and not bcrypt.check_password_hash(user['password'], data['password']):
        flash('Login unsuccessful. Please check email and password provided', 'warning')
        return redirect('login')
    elif not user:
        flash('Login unsuccessful. Please check email', 'warning')
        return render_template('login.html')


@app.route('/logout')
def logout():
    if 'user' in session:
        username = session['user']['name']
        session.pop('user')
        flash('We hope to see you soon {}'.format(username), 'info')
    else:
        flash('You are not logged in', 'warning')
    return redirect('home')


@app.route('/addrecipe')
def add_recipe():
    if 'user' not in session:
        flash('To add recipes, you need to login first', 'warning')
        return redirect('login')
    return render_template('addrecipe.html', foodtype=rcp_foodTypes, difficulties=rcp_diff)


@app.route('/insertrecipe', methods=['GET', 'POST'])
def insert_recipe():
    # Keep checking for active valid connection
    if 'user' not in session:
        flash('You are currently not logged in', 'warning')
        return redirect('login')

    # Create recipe Obj with required details
    data = request.form.to_dict()
    new_recipe = dict()

    # Main required recipe details
    new_recipe['author_id'] = ObjectId(session['user']['id'])
    new_recipe['name'] = data.pop('rcpname')
    new_recipe['description'] = data.pop('description')
    new_recipe['difficulty'] = data.pop('difficulty')
    new_recipe['serves'] = data.pop('serves')
    new_recipe['time'] = {"total": data.pop('time')}
    # initial views
    new_recipe['views'] = 0
    # add time creation/update
    new_recipe['updated'] = date.today().isoformat()

    # Add Ingredients
    match_ingr = re.compile("ingredient-")
    match_amt = re.compile("amount-")
    ingredients = [data[entry] for entry in sorted(data.keys()) if match_ingr.match(entry)]
    amount = [data[entry] for entry in sorted(data.keys()) if match_amt.match(entry)]
    ing_list = []
    for i in range(len(ingredients)):
        ing_list.append({"name": ingredients[i],
                         "amount": amount[i]})
    new_recipe['ingredients'] = ing_list

    # Add Steps
    match_step = re.compile("step-")
    steps = [data[entry] for entry in sorted(data.keys()) if match_step.match(entry)]
    # build list of dict to add image input later
    new_recipe['steps'] = [{"description": step} for step in steps]

    # Optional recipe details
    if "foodType" in data and data['foodType'] != "":
        new_recipe['foodType'] = data.pop('foodType')

    rcp = mongo.db.recipes.insert_one(new_recipe)

    # Add recipe's id to user's recipe list
    mongo.db.users.update({'_id': ObjectId(session['user']['id'])}, {'$push': {'recipes': rcp.inserted_id}})

    # Rename and store image using recipe's id
    pic = request.files['img']
    file_ext = pic.filename.rsplit('.', 1)[-1].lower()
    filename = str(rcp.inserted_id) + '.' + file_ext
    # double check file extension
    if not filename.endswith(pic_extensions):
        flash('wrong file extension', 'warning')
        return redirect('addrecipe')
    else:
        pic.save(path.join(app.config['RECIPE_PIC_DIR'], filename))

    # update recipe on db with image filename
    mongo.db.recipes.update({'_id': rcp.inserted_id}, {'$set': {'image': filename}})

    return redirect('/recipe/{}'.format(rcp.inserted_id))
