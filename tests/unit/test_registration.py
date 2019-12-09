"""
    *******************
    *     WARNING     *
    *******************

MAKE SURE TO RUN THESE TESTS WITH TEST FLAG IN CLI AS THEY ERASE DB ENTRIES:

'TEST=true python -m unittest tests/unit/test_registration.py'

or all unit tests :
'TEST=true python -m unittest discover -s tests/unit/'

"""
import unittest
from myzest import app, mongo, bcrypt
from flask import session, request


class TestRegistration(unittest.TestCase):
    """
    Tests user's registration data is well inserted in DB from '/add_user',
    then tests if user's session object is created successfully
    Tests submission with already registered details and wrong password confirmation
    """

    @classmethod
    def setUpClass(cls):
        mongo.db.users.delete_many({})

        cls.fake_user_entry = {
            'username': "john",
            'email': "John@gmail.com",
            'password': "1234",
            'passwConfirm': "1234"
        }

    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        mongo.db.users.delete_many({})

    @staticmethod
    def insert_fake_user(user):
        """ To implement DB with user data prior running test """
        inserted = mongo.db.users.insert_one({
            'username': user['username'].title(),
            'email': user['email'].lower(),
            'password': bcrypt.generate_password_hash(user['password'])
        })
        return mongo.db.users.find_one({'_id': inserted.inserted_id})

    def test_missing_form_data(self):
        """ App should redirect to register page if form data corrupted - missing field"""
        # Missing password confirmation field
        response = self.client.post('/add_user',
                                    data={'username': self.fake_user_entry['username'],
                                          'email': self.fake_user_entry['email'],
                                          'password': self.fake_user_entry['password']
                                          })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "http://localhost/register")

        # Missing password field
        response = self.client.post('/add_user',
                                    data={'username': self.fake_user_entry['username'],
                                          'email': self.fake_user_entry['email'],
                                          'passwConfirm': self.fake_user_entry['password']
                                          })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "http://localhost/register")

        # Missing password username field
        response = self.client.post('/add_user',
                                    data={'email': self.fake_user_entry['email'],
                                          'password': self.fake_user_entry['password'],
                                          'passwConfirm': self.fake_user_entry['password']
                                          })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "http://localhost/register")

        # Missing password email field
        response = self.client.post('/add_user',
                                    data={'username': self.fake_user_entry['username'],
                                          'password': self.fake_user_entry['password'],
                                          'passwConfirm': self.fake_user_entry['password']
                                          })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "http://localhost/register")

    def test_register_missmatched_passwords(self):
        """ App should redirect to registration page with error message about password confirmation """
        self.insert_fake_user(self.fake_user_entry)
        with self.client:
            response = self.client.post('/add_user',
                                        data={'username': self.fake_user_entry['username'],
                                              'email': self.fake_user_entry['email'],
                                              'password': self.fake_user_entry['password'],
                                              'passwConfirm': "wrong_password",
                                              },
                                        follow_redirects=True)
            self.assertEqual(str(request.url), "http://localhost/register")
            self.assertIn("Password confirmation do not match", str(response.data))

    def test_registration(self):
        """ Registration of new user should
        1. submit to DB: email in lower case, username capitalized,
        2. store username, id and 'favorites' list into session object
        3. redirect to home page
        """

        db_user = mongo.db.users.find_one({})
        self.assertEqual(db_user, None)  # this test should start with empty DB

        response = self.client.post('/add_user', data=self.fake_user_entry)
        db_user = mongo.db.users.find_one({})

        # 1. user data submission
        self.assertNotEqual(db_user['username'], self.fake_user_entry['username'])
        self.assertEqual(db_user['username'], self.fake_user_entry['username'].title())
        self.assertNotEqual(db_user['email'], self.fake_user_entry['email'])
        self.assertEqual(db_user['email'], self.fake_user_entry['email'].lower())
        self.assertNotEqual(db_user['password'], self.fake_user_entry['password'])
        self.assertTrue(bcrypt.check_password_hash(db_user['password'], self.fake_user_entry['password']))

        # 2. user data in session object
        with self.client:
            self.client.get('/')
            self.assertEqual(session['user'], {"username": db_user['username'],
                                               "_id": str(db_user['_id']),
                                               "favorites": []})
        # 3. redirection to home
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "http://localhost/home")

    def test_register_existing_username(self):
        """ App should redirect to registration page with error message about existing user """
        self.insert_fake_user(self.fake_user_entry)
        with self.client:
            response = self.client.post('/add_user',
                                        data={'username': "john",
                                              'email': "johnny@gmail.com",
                                              'password': "1234",
                                              'passwConfirm': "1234"},
                                        follow_redirects=True)
            self.assertEqual(str(request.url), "http://localhost/register")
            self.assertIn("This user already exists", str(response.data))

    def test_register_existing_email(self):
        """ App should redirect to registration page with error message about existing user """
        self.insert_fake_user(self.fake_user_entry)
        with self.client:
            response = self.client.post('/add_user',
                                        data={'username': "johnny",
                                              'email': "john@gmail.com",
                                              'password': "1234",
                                              'passwConfirm': "1234"},
                                        follow_redirects=True)
            self.assertEqual(str(request.url), "http://localhost/register")
            self.assertIn("This user already exists", str(response.data))
