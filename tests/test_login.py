import unittest
from myzest import app, mongo, bcrypt


class TestLogin(unittest.TestCase):
    """
    Test submitted Login data and DB data match.
    Last 3 tests are sequenced after user DB insert
    'test_wrong_email', 'test_wrong_password', 'test_login'
    """

    test_user = {'username': "Test Name",
                 'password': bcrypt.generate_password_hash("1234"),
                 'email': "test@mail.net"}

    def setUp(self):
        self.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        mongo.db.users.delete_many({})

    def test_failed_login(self):
        response = self.client.post('/log_usr', data=self.test_user, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Login unsuccessful. Please check email', str(response.data))

    def test_login(self):
        mongo.db.users.insert_one(self.test_user)
        response = self.client.post('/log_usr', data={'password': "1234",
                                                      'email': "test@mail.net"},
                                    follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome back Test Name !', str(response.data))

    def test_wrong_email(self):
        response = self.client.post('/log_usr', data={'password': "1234",
                                                      'email': "wrong_mail@mail.net"},
                                    follow_redirects=True)

        self.assertIn('Login unsuccessful. Please check email', str(response.data))

    def test_wrong_password(self):
        response = self.client.post('/log_usr', data={'password': "9876",
                                                      'email': "test@mail.net"},
                                    follow_redirects=True)

        self.assertIn('Login unsuccessful. Please check email and password provided',
                      str(response.data))


if __name__ == "__main__":
    unittest.main()
