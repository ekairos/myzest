"""
    *******************
    *     WARNING     *
    *******************

MAKE SURE TO RUN THESE TESTS WITH TEST FLAG IN CLI AS THEY ERASE DB ENTRIES:

'TEST=true python -m unittest tests/unit/test_urls.py'

or all unit tests :
'TEST=true python -m unittest discover -s tests/unit/'

"""

import unittest
from myzest import app, mongo
from tests.testing_data import fake_author, fake_recipe


class TestURLs(unittest.TestCase):
    """Tests view functions render or redirect to html pages as expected"""

    def setUp(self):
        self.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        mongo.db.recipes.delete_many({})
        mongo.db.users.delete_many({})

    def test_root_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_route(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)

    def test_login_route(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_register_route(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_recipe_route(self):
        """ '/recipe' needs a recipe id as path variable
         '/recipe/<recipe_id> """
        response = self.client.get('/recipe/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "http://localhost/error")

        mongo.db.users.insert_one(fake_author)
        # ins_author = mongo.db.users.insert_one({})

        ins_rcp = mongo.db.recipes.insert_one(fake_recipe)
        # ins_rcp = mongo.db.recipes.find_one({})

        self.client.get('/')
        response = self.client.get('/recipe/{}'.format(ins_rcp.inserted_id))
        self.assertEqual(response.status_code, 200)

    def test_failed_add_recipe(self):
        """ App should redirect anonymous user to login page """
        response = self.client.get('/addrecipe')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], 'http://localhost/login')

    def test_fake_endpoint(self):
        """ App should redirect to error page if url is incorrect """
        response = self.client.get('/fake')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], 'http://localhost/error')
