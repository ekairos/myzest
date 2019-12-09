"""
    *******************
    *     WARNING     *
    *******************

MAKE SURE TO RUN THESE TESTS WITH TEST FLAG IN CLI AS THEY ERASE DB ENTRIES:
Run in two separate terminals:
'TEST=true python run.py'
and
'TEST=true python -m unittest tests/e2e/test_user_register.py'

"""
import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from myzest import mongo, bcrypt


class TestRegistration(unittest.TestCase):
    """ Tests user registration process
    1. User navs to registration
    2. Tests registration form feedbacks with various inputs
    3. Submit valid register form and check url redirection
    """

    @classmethod
    def setUpClass(cls):
        mongo.db.users.insert_one({'username': 'John',
                                   'email': 'john@gmail.com',
                                   'password': bcrypt.generate_password_hash('1234').decode('utf-8'),
                                   'favorites': [],
                                   'avatar': 'default.png'})

    @classmethod
    def tearDownClass(cls):
        """Delete data after registration to keep tests independent"""
        mongo.db.users.delete_many({})

    def setUp(self):
        # CHROME SETUP
        # self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_options.add_experimental_option("detach", True)
        # self.driver = webdriver.Chrome(desired_capabilities=self.chrome_options.to_capabilities())
        # self.driver = webdriver.Chrome()

        # FIREFOX SETUP
        self.driver = webdriver.Firefox()

        # Device screen size
        self.driver.set_window_size(360, 640)

        self.actions = ActionChains(self.driver)

    def tearDown(self):
        self.driver.close()

    def test_user_registration(self):
        """Tests registration process
        1. Anonymous user nav to registration page
        2. Test form validation with various inputs
        3. Test valid registration submission
        """

        # NAV TO REGISTRATION
        self.driver.get("http://localhost:5000/")
        burger = self.driver.find_element_by_css_selector(".sidenav-trigger.right")
        rego_nav = self.driver.find_element_by_xpath("//ul[@id='side-menu']/li[4]/a[@href='/register']")

        burger.click()
        rego_nav.click()
        self.assertEqual(self.driver.current_url, "http://localhost:5000/register")

        self.driver.set_script_timeout(1)

        # FILL REGISTER FORM
        # Interactive element pointers
        username_field = self.driver.find_element_by_id("reg-username")
        username_help = self.driver.find_element_by_id("username_help")
        email_field = self.driver.find_element_by_id("reg-email")
        email_help = self.driver.find_element_by_id("email_help")
        password_field = self.driver.find_element_by_id("reg-password")
        password_help = self.driver.find_element_by_xpath("//form[@id='registration']/div[3]/span")
        pass_confirm_field = self.driver.find_element_by_id("reg-passwConfirm")
        password_confirm_help = self.driver.find_element_by_xpath("//form[@id='registration']/div[4]/span")

        # test wrong username format
        username_field.send_keys("john@gmail.com", Keys.TAB)
        self.assertEqual(username_field.get_attribute("class"), "validate invalid")
        self.assertEqual(username_help.get_attribute("data-error"),
                         "Invalid format, please match up to two words of 15 letters each")

        # test registered username
        username_field.clear()
        username_field.send_keys("John", Keys.TAB)
        sleep(1)
        self.assertEqual(username_field.get_attribute("class"), "validate invalid")
        self.assertEqual(username_help.get_attribute("data-error"), "This username is already taken")

        # test empty username
        username_field.clear()
        username_field.send_keys(Keys.TAB)
        self.assertEqual(username_help.get_attribute("data-error"), "This field is required")

        # test unregistered username
        username_field.clear()
        username_field.send_keys("Billy", Keys.TAB)
        sleep(0.5)
        self.assertEqual(username_field.get_attribute("class"), "validate valid")

        # test wrong email format
        email_field.send_keys("Billy")
        username_field.send_keys(Keys.TAB)
        self.assertEqual(email_field.get_attribute("class"), "validate invalid")
        self.assertEqual(email_help.get_attribute("data-error"), "Invalid email format")

        # test registered email
        email_field.clear()
        email_field.send_keys("john@gmail.com")
        username_field.send_keys(Keys.TAB)
        sleep(1)
        self.assertEqual(email_field.get_attribute("class"), "validate invalid")
        self.assertEqual(email_help.get_attribute("data-error"), "This email is already taken")

        # test empty email
        email_field.clear()
        username_field.send_keys(Keys.TAB)
        self.assertEqual(email_help.get_attribute("data-error"), "This field is required")

        # test unregistered email
        email_field.clear()
        email_field.send_keys("billy@gmail.com")
        username_field.send_keys(Keys.TAB)
        sleep(0.5)
        self.assertEqual(email_field.get_attribute("class"), "validate valid")

        # test mismatch password confirmation
        password_field.send_keys("1234")
        pass_confirm_field.send_keys("5678", Keys.TAB)
        self.assertEqual(password_help.get_attribute("data-error"), "Passwords do not match")
        self.assertEqual(password_confirm_help.get_attribute("data-error"), "Passwords do not match")

        # test submission
        password_field.clear()
        password_field.send_keys("1234")
        pass_confirm_field.clear()
        pass_confirm_field.send_keys("1234")
        submit_btn = self.driver.find_element_by_xpath("//form[@id='registration']/div[5]/button")
        self.actions.move_to_element(submit_btn).perform()
        submit_btn.click()
        WebDriverWait(self.driver, 3).until(EC.url_to_be("http://localhost:5000/home"))
        self.assertEqual(self.driver.current_url, "http://localhost:5000/home")
        self.assertEqual(self.driver.find_element_by_css_selector(".flash-success").text,
                         "Welcome Billy ! Your account was created with billy@gmail.com")


if __name__ == '__main__':
    unittest.main()
