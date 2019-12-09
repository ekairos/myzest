"""
    *******************
    *     WARNING     *
    *******************

MAKE SURE TO RUN THESE TESTS WITH TEST FLAG IN CLI AS THEY ERASE DB ENTRIES:
Run in two separate terminals:
'TEST=true python run.py'
and
'TEST=true python -m unittest tests/e2e/test_user_login.py'

"""
import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from myzest import mongo, bcrypt


class TestLogin(unittest.TestCase):
    """ Tests user login process
    1. User nav to login page
    2. Test UI feedbacks when filling login form with various wrong inputs
    3. Submits form with valid credentials """

    @classmethod
    def setUpClass(cls):
        cls.billy = mongo.db.users.insert_one({'username': 'Billy',
                                               'email': 'billy@gmail.com',
                                               'password': bcrypt.generate_password_hash('1234').decode('utf-8'),
                                               'favorites': [],
                                               'avatar': 'default.png'})

    @classmethod
    def tearDownClass(cls):
        mongo.db.users.delete_one({'_id': cls.billy.inserted_id})

    def setUp(self):
        # CHROME SETUP
        # self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_options.add_experimental_option("detach", True)
        # self.driver = webdriver.Chrome(desired_capabilities=self.chrome_options.to_capabilities())

        # FIREFOX SETUP
        self.driver = webdriver.Firefox()

        # Device screen size
        self.driver.set_window_size(360, 640)

    def tearDown(self):
        self.driver.close()

    def test_user_login(self):
        """Tests login process
        1. User nav to login page
        2. Fill form with various inputs
        3. Submit valid login form
        """

        # NAV TO LOGIN
        self.driver.get("http://localhost:5000/")
        burger = self.driver.find_element_by_css_selector(".sidenav-trigger.right")
        login_nav = self.driver.find_element_by_xpath("//ul[@id='side-menu']/li[4]/a[@href='/login']")

        burger.click()
        login_nav.click()
        WebDriverWait(self.driver, 2).until(EC.url_changes)
        self.assertEqual(self.driver.current_url, "http://localhost:5000/login")

        # FILL LOGIN
        # Interactive element pointers
        login_field = self.driver.find_element_by_id("log-email")
        email_help = self.driver.find_element_by_id("email_help")
        password_field = self.driver.find_element_by_id("log-password")
        password_help = self.driver.find_element_by_xpath("//form[@id='login']/div[2]/span")
        submit_button = self.driver.find_element_by_xpath("//form[@id='login']/div[3]/button")

        # test wrong email format
        login_field.send_keys("thomas", Keys.TAB)
        self.assertEqual(login_field.get_attribute("class"), "validate invalid")
        self.assertEqual(email_help.get_attribute("data-error"), "Invalid email format")

        # test unregistered email
        login_field.clear()
        login_field.send_keys("thomas@gmail.com", Keys.TAB)
        sleep(0.5)
        self.assertEqual(login_field.get_attribute("class"), "validate invalid")
        self.assertEqual(email_help.get_attribute("data-error"), "This email is not registered")

        # test registered email
        login_field.clear()
        login_field.send_keys("billy@gmail.com", Keys.TAB)
        sleep(0.5)
        self.assertEqual(login_field.get_attribute("class"), "validate valid")

        # test empty password
        password_field.send_keys(Keys.TAB)
        self.assertEqual(password_help.get_attribute("data-error"), "This field is required")

        # test login with wrong password
        password_field.send_keys("0000")
        submit_button.click()
        sleep(1)
        self.assertEqual(self.driver.current_url, "http://localhost:5000/login")
        self.assertEqual(self.driver.find_element_by_css_selector(".flash-warning").text,
                         "Login unsuccessful. Please check email and password provided")

        # test login with valid credentials
        login_field = self.driver.find_element_by_id("log-email")
        password_field = self.driver.find_element_by_id("log-password")
        submit_button = self.driver.find_element_by_xpath("//form[@id='login']/div[3]/button")

        login_field.clear()
        login_field.send_keys("billy@gmail.com", Keys.TAB)
        password_field.clear()
        password_field.send_keys("1234")
        submit_button.click()
        WebDriverWait(self.driver, 3).until(EC.url_changes)
        self.assertEqual(self.driver.current_url, "http://localhost:5000/home")
        self.assertEqual(self.driver.find_element_by_css_selector(".flash-success").text,
                         "Welcome back Billy !")


if __name__ == "__main__":
    unittest.main()
