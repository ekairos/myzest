"""
    *******************
    *     WARNING     *
    *******************

MAKE SURE TO RUN THESE TESTS WITH TEST FLAG IN CLI AS THEY ERASE DB ENTRIES:
Run in two separate terminals:
'TEST=true python run.py'
and
'TEST=true python -m unittest tests/e2e/test_user_delete.py'

"""
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
from myzest import mongo, bcrypt


class TestDeleteUser(unittest.TestCase):
    """Tests a user deleting his account
    1. User nav to profile
    2. User follow deletion process
    3. User login unsuccessful with email error message
    4. Check user's username and email availability in register form
    """

    @classmethod
    def setUpClass(cls):
        cls.billy = mongo.db.users.insert_one({'username': 'Billy',
                                               'email': 'billy@gmail.com',
                                               'password': bcrypt.generate_password_hash('1234').decode('utf-8'),
                                               'favorites': [],
                                               'avatar': 'default.png'})

    @classmethod
    def tearDownClass(cls):
        """Clean DB in case test execution is interrupted"""
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

        self.actions = ActionChains(self.driver)

    def tearDown(self):
        self.driver.close()

    def nav_to_login(self):
        """Should nav to login page"""
        self.driver.get("http://localhost:5000/")
        self.driver.find_element_by_css_selector(".sidenav-trigger.right").click()
        self.driver.find_element_by_xpath("//ul[@id='side-menu']/li[4]/a[@href='/login']").click()
        WebDriverWait(self.driver, 2).until(EC.url_changes)
        self.assertEqual(self.driver.current_url, "http://localhost:5000/login")

    def login_user(self):
        """Submitting billy's credential, assertions in test function"""
        self.driver.find_element_by_id("log-email").send_keys("billy@gmail.com")
        self.driver.find_element_by_id("log-password").send_keys("1234")
        self.driver.find_element_by_xpath("//form[@id='login']/div[3]/button").click()

    def nav_to_profile(self):
        """Should nav to profile page"""
        self.driver.find_element_by_css_selector(".sidenav-trigger.right").click()
        self.driver.find_element_by_xpath("//ul[@id='side-menu']/li[3]/a").click()
        WebDriverWait(self.driver, 3).until(EC.url_changes)
        self.assertRegex(self.driver.current_url, "^http://localhost:5000/profile/")

    def to_edit_profile(self):
        """Should nav to edit profile page"""
        self.driver.find_element_by_css_selector("#profile a.btn-floating").click()
        WebDriverWait(self.driver, 3).until(EC.url_changes)
        self.assertRegex(self.driver.current_url, "^http://localhost:5000/edit-profile/")

    def delete_account(self):
        height = self.driver.execute_script("return document.body.scrollHeight")
        self.driver.execute_script("window.scrollTo(0, {});".format(height))
        delete = self.driver.find_element_by_css_selector("a[href='#del-account']")
        self.actions.move_to_element(delete).perform()
        sleep(0.5)
        delete.click()
        self.assertEqual(self.driver.find_element_by_id("del-account").is_displayed(), True)
        self.driver.find_element_by_css_selector("#del-account a.modal-close").click()
        sleep(0.5)
        self.assertEqual(self.driver.find_element_by_id("del-account").is_displayed(), False)
        delete.click()
        self.driver.find_element_by_css_selector("#del-account a.btn-cancel").click()
        WebDriverWait(self.driver, 2).until(EC.url_changes)
        self.assertRegex(self.driver.current_url, "^http://localhost:5000/home")
        self.assertEqual(self.driver.find_element_by_css_selector(".flash-info").text,
                         "We are sorry to see you leave Billy. Feel free to come back anytime !")

    def check_register(self):
        """ Should nav to register page
            Register form's validation should mark fields valid as absent in database
        """
        self.driver.find_element_by_css_selector(".sidenav-trigger.right").click()
        self.driver.find_element_by_xpath("//ul[@id='side-menu']/li[3]/a[@href='/register']").click()
        WebDriverWait(self.driver, 2).until(EC.url_changes)
        self.assertEqual(self.driver.current_url, "http://localhost:5000/register")
        self.driver.find_element_by_id("reg-username").send_keys("Billy")
        self.driver.find_element_by_id("reg-email").send_keys("billy@gmail.com", Keys.TAB)
        sleep(0.5)
        self.assertEqual(self.driver.find_element_by_id("reg-username")
                         .get_attribute("class"), "validate valid")
        self.assertEqual(self.driver.find_element_by_id("reg-email")
                         .get_attribute("class"), "validate valid")

    def test_user_delete(self):
        # 1. to profile
        self.nav_to_login()
        self.login_user()
        WebDriverWait(self.driver, 3).until(EC.url_changes)
        self.assertEqual(self.driver.current_url, "http://localhost:5000/home")
        self.nav_to_profile()
        # 2. delete account
        self.to_edit_profile()
        self.delete_account()
        # 3. try login
        self.nav_to_login()
        self.login_user()
        self.assertEqual(self.driver.current_url, "http://localhost:5000/login")
        self.assertEqual(self.driver.find_element_by_css_selector(".flash-warning").text,
                         "Login unsuccessful. Please check email and password provided")
        # 4. check username and email availability in db
        self.check_register()


if __name__ == "__main__":
    unittest.main()
