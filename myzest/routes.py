from flask import render_template, request, jsonify, redirect, flash, session
from myzest import app, mongo, bcrypt
from bson.objectid import ObjectId
import re
import json
from datetime import date
from os import path


rcp_diff = ("easy", "average", "hard")
rcp_foodTypes = mongo.db.foodtype.distinct("name")
rcp_foodTypes.sort()
rcp_foodCategories = mongo.db.category.distinct("name")
rcp_foodCategories.sort()

pic_extensions = ("jpg", "jpeg", "png", "gif")


# Override to serialize ObjectIds data from DB
# into str for user's session object
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route('/')
@app.route('/home')
def home():
    recipes = mongo.db.recipes.find()
    return render_template('home.html', recipes=recipes)


@app.route('/recipe/<recipe_id>')
def get_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    author = mongo.db.users.find_one({'_id': ObjectId(recipe['author_id'])})
    mongo.db.recipes.update({'_id': ObjectId(recipe_id)}, {'$inc': {'views': 1}})
    return render_template('recipe.html', recipe=recipe, author=author)


@app.route('/register')
def register():
    if 'user' in session:
        flash('{}, you are already logged in'.format(session['user']['username']), 'info')
        return redirect('home')
    return render_template('register.html')


@app.route('/add_user', methods=['POST'])
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
        # start first session with 'username' and '_id' only
        session['user'] = {'username': new_user['username'], '_id': str(registered_user.inserted_id)}
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


@app.route('/login')
def login():
    if 'user' in session:
        flash('{}, you are already logged in'.format(session['user']['username']), 'info')
        return redirect('home')
    return render_template('login.html')


@app.route('/log_usr', methods=['POST'])
def log_usr():
    data = request.form.to_dict()
    user_in_db = mongo.db.users.find_one({'email': data['email']})
    if user_in_db and bcrypt.check_password_hash(user_in_db['password'], data['password']):
        user = mongo.db.users.find_one({'_id': user_in_db['_id']}, {'username': 1, 'favorites': 1})
        user = JSONEncoder().encode(user)
        session['user'] = json.loads(user)
        flash('Welcome back {} !'.format(user_in_db['username']), 'success')
        return redirect('home')
    elif user_in_db and not bcrypt.check_password_hash(user_in_db['password'], data['password']):
        flash('Login unsuccessful. Please check email and password provided', 'warning')
        return redirect('login')
    elif not user_in_db:
        flash('Login unsuccessful. Please check email', 'warning')
        return render_template('login.html')


@app.route('/logout')
def logout():
    if 'user' in session:
        username = session['user']['username']
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
    new_recipe['author_id'] = ObjectId(session['user']['_id'])
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
    mongo.db.users.update({'_id': ObjectId(session['user']['_id'])}, {'$push': {'recipes': rcp.inserted_id}})

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


@app.route('/del_rcp/<recipe_id>')
def del_rcp(recipe_id):
    mongo.db.users.update({"_id": ObjectId(session['user']['id'])}, {'$pull': {'recipes': ObjectId(recipe_id)}})
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    return redirect('/home')


@app.route('/update_rcp/<recipe_id>', methods=['GET', 'POST'])
def update_rcp(recipe_id):
    this_recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    if request.method == 'POST':
        # Keep checking for active valid connection
        if 'user' not in session:
            flash('Sorry the connection was lost, please login', 'warning')
            return redirect('login')

        # Create recipe Obj with main required details
        data = request.form.to_dict()
        upd_recipe = dict()

        upd_recipe['author_id'] = ObjectId(session['user']['_id'])
        upd_recipe['name'] = data.pop('rcpname')
        upd_recipe['description'] = data.pop('description')
        upd_recipe['difficulty'] = data.pop('difficulty')
        upd_recipe['serves'] = data.pop('serves')
        upd_recipe['time'] = {"total": data.pop('time')}
        upd_recipe['views'] = this_recipe['views']

        # Add Ingredients
        match_ingr = re.compile("ingredient-")
        match_amt = re.compile("amount-")
        ingredients = [data[entry] for entry in sorted(data.keys()) if match_ingr.match(entry)]
        amount = [data[entry] for entry in sorted(data.keys()) if match_amt.match(entry)]
        ing_list = []
        for i in range(len(ingredients)):
            ing_list.append({"name": ingredients[i],
                             "amount": amount[i]})
        upd_recipe['ingredients'] = ing_list

        # Add Steps
        match_step = re.compile("step-")
        steps = [data[entry] for entry in sorted(data.keys()) if match_step.match(entry)]
        # build list of dict to add image input later
        upd_recipe['steps'] = [{"description": step} for step in steps]

        # update last modified
        upd_recipe['updated'] = date.today().isoformat()

        # Optional recipe details
        if data['foodType'] != "none":
            upd_recipe['foodType'] = data.pop('foodType')

        # Keep image file from previous version
        pic = request.files['img'].filename
        if pic != "":
            file_ext = pic.rsplit('.', 1)[-1].lower()
            filename = str(this_recipe['_id']) + '.' + file_ext
            # double check for valid file extension
            if not filename.endswith(pic_extensions):
                flash('wrong file extension', 'warning')
                return redirect('/update_rcp/{}'.format(recipe_id))
            else:
                upd_recipe['image'] = filename
                request.files['img'].save(path.join(app.config['RECIPE_PIC_DIR'], filename))
        else:
            upd_recipe['image'] = this_recipe['image']

        # Update this recipe on DB
        mongo.db.recipes.replace_one({'_id': this_recipe['_id']}, upd_recipe)

        return redirect('/recipe/{}'.format(recipe_id))

    return render_template('updaterecipe.html', recipe=this_recipe, foodtypes=rcp_foodTypes, difficulties=rcp_diff)
