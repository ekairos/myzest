import unittest
from myzest import app, mongo, bcrypt
from flask import session


class TestLogin(unittest.TestCase):
    """
    Test submitted Login data and DB data match.
    Last 3 tests are sequenced after user DB insert
    'test_login', 'test_wrong_email', 'test_wrong_password'
    """

    @classmethod
    def setUpClass(cls):
        cls.fake_user = {'username': "John",
                         'password': "1234",
                         'email': "john@mail.net"}

    def setUp(self):
        self.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        mongo.db.users.delete_many({})

    @staticmethod
    def user_to_db(user):
        user_to_db = user.copy()
        user_to_db['password'] = bcrypt.generate_password_hash(user_to_db['password'])
        return mongo.db.users.insert_one(user_to_db)

    def test_failed_login(self):
        """ Login with unregistered user data should fail """
        response = self.client.post('/log_usr', data=self.fake_user, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Login unsuccessful. Please check email', str(response.data))

    def test_login(self):
        """
        Login with registered user data should succeed;
        session object should contain user's 'username' '_id' and 'favs' list;
        A views list object should be created in session object;
        """
        self.user_in_db = self.user_to_db(self.fake_user)

        with self.client:
            self.client.get('/')
            response = self.client.post('/log_usr', data={'password': self.fake_user['password'],
                                                          'email': self.fake_user['email']},
                                        follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Welcome back John !', str(response.data))

            self.client.get('/')
            self.assertEqual(session['user']['username'], self.fake_user['username'])
            self.assertEqual(session['user']['_id'], str(self.user_in_db.inserted_id))
            self.assertEqual(session['views'], [])

    def test_wrong_email(self):
        """ Login should fail on wrong email submission """
        response = self.client.post('/log_usr', data={'password': self.fake_user['password'],
                                                      'email': "wrong_mail@mail.net"},
                                    follow_redirects=True)

        self.assertIn('Login unsuccessful. Please check email', str(response.data))

    def test_wrong_password(self):
        """ Login should fail on wrong password submission """
        response = self.client.post('/log_usr', data={'password': "9876",
                                                      'email': self.fake_user['email']},
                                    follow_redirects=True)

        self.assertIn('Login unsuccessful. Please check email and password provided',
                      str(response.data))
