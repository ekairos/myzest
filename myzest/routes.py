from flask import render_template, request, jsonify, redirect, flash
from myzest import app, mongo, bcrypt
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    data = request.form.to_dict()
    print(data)
    hashed_passw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = {
        'username': data['username'].title(),
        'email': data['email'].lower(),
        'password': hashed_passw
    }
    print('new user ', new_user)
    query = mongo.db.users.find_one({"$or":[{"username": new_user["username"]}, {"email": new_user["email"]}]})
    print('query name ', query)
    if query:
        print('found it')
        flash('This user already exists', 'warning')
    elif query is None:
        print('nothing found')
        mongo.db.users.insert_one(new_user)
        flash('Welcome {} ! Your account was created with {}'
              .format(new_user['username'], new_user['email']), 'success')
    return redirect('home')


@app.route('/check_usr', methods=['POST'])
def check_usr():
    data = request.get_json()
    if 'username' in data:
        if mongo.db.users.find_one({'username': data['username'].title()}):
            return jsonify({'error': 'username', 'message': 'This username is already taken'})
    if 'email' in data:
        email = mongo.db.users.find_one({'email': data['email'].lower()})
        if data['form'] == "registration" and email is not None:
            return jsonify({'error': 'email', 'message': 'This email is already in use'})
        if data['form'] == "login" and email is None:
            return jsonify({'error': 'email', 'message': 'This email is not registered'})
    return 'success'


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/log_usr', methods=['GET', 'POST'])
def log_usr():
    data = request.form.to_dict()
    user = mongo.db.users.find_one({"email": data["email"]})
    if user and bcrypt.check_password_hash(user['password'], data['password']):
        flash('Welcome back {} !'.format(user['username']), 'success')
        return redirect('home')
    elif user and not bcrypt.check_password_hash(user['password'], data['password']):
        flash('Login unsuccessful. Please check email and password provided', 'warning')
        return redirect('login')
    elif not user:
        flash('Login unsuccessful. Please check email', 'warning')
        return render_template('login.html')
