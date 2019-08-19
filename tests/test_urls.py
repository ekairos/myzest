import unittest
from myzest import app


class TestURLs(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_root_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_route(self):
        response = self.app.get('/home')
        self.assertEqual(response.status_code, 200)

    def test_login_route(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_register_route(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_recipe_route(self):
        """ '/recipe' needs a recipe id as path variable
         '/recipe/<recipe_id> """
        response = self.app.get('/recipe/')
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
