import unittest
from myzest import app, mongo, bcrypt
from flask import session


class TestRegistration(unittest.TestCase):
    """
    Tests user's registration data is inserted in DB from '/add_user'
    Then tests if user's session object is created successfully
    """

    @classmethod
    def setUpClass(cls):
        mongo.db.users.delete_many({})

    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        mongo.db.users.delete_one({"username": self.test_user['username']})

    def user_test(self, username, password, email):
        self.test_user = {'username': username,
                          'password': password,
                          'email': email}
        return self.test_user

    def test_registration(self):
        self.user_test("Test Name", "1234", "mail@gmail.com")

        db_user = mongo.db.users.find_one({})
        self.assertEqual(db_user, None)

        response = self.client.post('/add_user', data=self.test_user)
        self.assertEqual(response.status_code, 302)

        db_user = mongo.db.users.find_one({})
        self.assertEqual(db_user['username'], self.test_user['username'])
        self.assertEqual(db_user['email'], self.test_user['email'])
        self.assertTrue(bcrypt.check_password_hash(db_user['password'], self.test_user['password']))

        with self.client:
            self.client.get('/')
            self.assertEqual(session['user'], {"username": db_user['username'],
                                               "_id": str(db_user['_id'])})
