"""
    *******************
    *     WARNING     *
    *******************

MAKE SURE TO RUN THESE TESTS WITH TEST FLAG IN CLI AS THEY ERASE DB ENTRIES:

'TEST=true python -m unittest tests/unit/test_login.py'

or all unit tests :
'TEST=true python -m unittest discover -s tests/unit/'

"""
import unittest
from myzest import app, mongo, bcrypt
from flask import session, request


class TestLogin(unittest.TestCase):
    """ Test user login with unregistered email, wrong password and missing input.
    On successful login, the app should decrement users recipe view count if user viewed his own recipe prior login;
    """

    @classmethod
    def setUpClass(cls):
        cls.fake_user = {'username': 'John',
                         'email': "john@mail.net",
                         'password': "1234",
                         'passwConfirm': "1234"}

    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        mongo.db.users.delete_many({})
        mongo.db.recipes.delete_many({})

    @staticmethod
    def user_to_db(user):
        """To insert a fake user into DB prior tests."""

        return mongo.db.users.insert_one({
            'username': user['username'].title(),
            'email': user['email'].lower(),
            'password': bcrypt.generate_password_hash(user['password'])
        })

    def test_failed_login(self):
        """ Login with unregistered email should fail and redirect to login """

        with self.client:
            response = self.client.post('/log_user',
                                        data={'email': self.fake_user['email'],
                                              'password': self.fake_user['password']},
                                        follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(str(request.url), "http://localhost/login")
            self.assertIn('Login unsuccessful. Please check email', str(response.data))

    def test_login(self):
        """
        Login with registered user data should redirect to home page by default and store user's id,
        username and favorites recipe list in session object;
        """

        user_in_db = self.user_to_db(self.fake_user)

        with self.client:
            self.client.get('/')
            response = self.client.post('/log_user',
                                        data={'email': self.fake_user['email'],
                                              'password': self.fake_user['password']},
                                        follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Welcome back John !', str(response.data))

            self.client.get('/')
            self.assertEqual(session['user']['username'], self.fake_user['username'])
            self.assertEqual(session['user']['_id'], str(user_in_db.inserted_id))

    def test_wrong_email(self):
        """ On wrong email submission app should redirect to login page with
        error message about email
        """

        with self.client:
            response = self.client.post('/log_user',
                                        data={'password': self.fake_user['password'],
                                              'email': "wrong_mail@mail.net"},
                                        follow_redirects=True)
            self.assertEqual(str(request.url), "http://localhost/login")
            self.assertIn('Login unsuccessful. Please check email', str(response.data))

    def test_wrong_password(self):
        """ On wrong password submission app should redirect to login page with
        error message about credentials
        """

        self.user_to_db(self.fake_user)
        with self.client:
            response = self.client.post('/log_user',
                                        data={'password': "9876",
                                              'email': self.fake_user['email']},
                                        follow_redirects=True)
            self.assertEqual(str(request.url), "http://localhost/login")
            self.assertIn('Login unsuccessful. Please check email and password provided',
                          str(response.data))

    def test_missing_email(self):
        """Without an email provided, app should redirect to login with
        error message.
        """

        self.user_to_db(self.fake_user)
        with self.client:
            response = self.client.post('/log_user',
                                        data={'password': self.fake_user['password']},
                                        follow_redirects=True)
            self.assertEqual(str(request.url), "http://localhost/login")
            self.assertIn('Login unsuccessful. Please provide both email and password',
                          str(response.data))

    def test_missing_password(self):
        """ App should redirect to login by default if password if missing."""

        self.user_to_db(self.fake_user)
        with self.client:
            response = self.client.post('/log_user',
                                        data={'email': self.fake_user['email']},
                                        follow_redirects=True)
            self.assertEqual(str(request.url), "http://localhost/login")
            self.assertIn('Login unsuccessful. Please provide both email and password',
                          str(response.data))
