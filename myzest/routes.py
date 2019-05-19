from flask import render_template
from myzest import app


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', page="home page")
