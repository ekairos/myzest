import unittest
from myzest import app


class TestURLs(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        pass

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

    def test_failed_add_recipe(self):
        """ App should redirect to login anonymous user """
        response = self.client.get('/addrecipe')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], 'http://localhost/login')
