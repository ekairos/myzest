# MyZest

**_Live preview_** [on Heroku](https://myzest.herokuapp.com/)       

Table Of Content

- [Overview](#overview)
- [License](#license)


## Overview

**MyZest** is an online cookbook.  
It allows any users to find any recipes that their author wishes to share through this app.  
Authenticated users can save, share and retrieve any recipes on MyZest.  
Recipes author has the possibility to change the privacy of any of their recipes at any time. Keeping a recipe secret or share it with MyZest community.  


## Features

### Implemented features

- User Registration and Login.
- CRUD operations on recipes.
- User favorite recipes.
- User search, filter and order recipes.
- Pagination.

### Features to add

- Recipe's privacy.
- Recipe rating.
( According to recent UX studies, 5star scoring system might replaced ).
- User profile page.


## Main Tech Used

### Back-end

- [Python 3.5](https://docs.python.org/3/whatsnew/3.5.html)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/) framework.
- [MongoDB](http://mongodb.org)
    - I use MongoDB Atlas to host recipes and users data.
    - [PyMongo](https://api.mongodb.com/python/current/) is used through the [Flask-PyMongo](https://flask-pymongo.readthedocs.io/) extension.

### Front-end

- Styling is written in [SCSS](https://sass-lang.com)
- [MaterializeCSS](https://materializecss.com/)
    - The **MaterializeCSS** framework provides default styling and animations as a good starting point.
- [jQuery](https://jquery.com/)
	- **jQuery** library is used to ease DOM manipulation.


## License

This project is licensed under the MIT License.
See the [LICENSE.md](./LICENSE.md) file for license rights and limitations (MIT).
