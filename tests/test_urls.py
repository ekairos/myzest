import unittest
from myzest import app, mongo
import json


class TestURLs(unittest.TestCase):

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
        self.assertEqual(response.status_code, 404)

        author_file = open('tests/fake_user.json', 'r')
        author = json.load(author_file)
        ins_author = mongo.db.users.insert_one(author)
        author_file.close()

        rcp_file = open('tests/fake_recipe.json', 'r')
        recipe = json.load(rcp_file)
        recipe['author_id'] = ins_author.inserted_id
        ins_rcp = mongo.db.recipes.insert_one(recipe)
        rcp_file.close()

        self.client.get('/')
        response = self.client.get('/recipe/{}'.format(ins_rcp.inserted_id))
        self.assertEqual(response.status_code, 200)

    def test_failed_add_recipe(self):
        """ App should redirect to login anonymous user """
        response = self.client.get('/addrecipe')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], 'http://localhost/login')
