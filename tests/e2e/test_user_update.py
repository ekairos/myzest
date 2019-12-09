"""
    *******************
    *     WARNING     *
    *******************

MAKE SURE TO RUN THESE TESTS WITH TEST FLAG IN CLI AS THEY ERASE DB ENTRIES:
Run in two separate terminals:
'TEST=true python run.py'
and
'TEST=true python -m unittest tests/e2e/test_user_update.py'

"""
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from myzest import mongo, bcrypt


class TestUpdateUser(unittest.TestCase):
    """Tests a user updating his profile
    1. User nav to profile (with no bio)
    2. User adds a bio
    3. Checks the bio is readable in user's profile
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

    def nav_to_login(self):
        """Should nav to login page"""
        self.driver.get("http://localhost:5000/")
        self.driver.find_element_by_css_selector(".sidenav-trigger.right").click()
        self.driver.find_element_by_xpath("//ul[@id='side-menu']/li[5]/a[@href='/login']").click()
        WebDriverWait(self.driver, 2).until(EC.url_changes)
        self.assertEqual(self.driver.current_url, "http://localhost:5000/login")

    def login_user(self):
        """Submitting valid login form takes user to home page"""
        self.driver.find_element_by_id("log-email").send_keys("billy@gmail.com")
        self.driver.find_element_by_id("log-password").send_keys("1234")
        self.driver.find_element_by_xpath("//form[@id='login']/div[3]/button").click()
        WebDriverWait(self.driver, 2).until(EC.url_changes)
        self.assertEqual(self.driver.current_url, "http://localhost:5000/home")

    def nav_to_profile(self):
        """Should nav to profile page"""
        self.driver.find_element_by_css_selector(".sidenav-trigger.right").click()
        self.driver.find_element_by_xpath("//ul[@id='side-menu']/li[4]/a").click()
        WebDriverWait(self.driver, 2).until(EC.url_changes)
        self.assertRegex(self.driver.current_url, "^http://localhost:5000/profile/")
        self.assertEqual(self.driver.find_element_by_css_selector("#profile p").text, "Add something about you.")

    def to_edit_profile(self):
        """
        Should nav between profile and edit-profile pages
        1. From edit floating btn
        2. Cancel button in edit profile pages takes user back to profile
        3. browser's go back and forwards button should lead back to profile page
        4. 'Add something' link in empty bio takes user to edit profile page with form pre-filled
        """
        # 1. To edit profile page
        self.driver.find_element_by_css_selector("#profile a.btn-floating").click()
        WebDriverWait(self.driver, 2).until(EC.url_changes)
        self.assertRegex(self.driver.current_url, "^http://localhost:5000/edit-profile/")
        # 2. Form cancel btn back to profile
        self.driver.find_element_by_css_selector("#editprofile footer button a").click()
        WebDriverWait(self.driver, 2).until(EC.url_changes)
        self.assertRegex(self.driver.current_url, "^http://localhost:5000/profile/")
        # 3. Browser's back and forward navigation
        self.driver.back()
        WebDriverWait(self.driver, 2).until(EC.url_changes)
        self.assertRegex(self.driver.current_url, "^http://localhost:5000/edit-profile/")
        self.driver.forward()
        WebDriverWait(self.driver, 2).until(EC.url_changes)
        self.assertRegex(self.driver.current_url, "^http://localhost:5000/profile/")
        # 4. 'Add something' link in profile (empty) bio nav to edit-profile page
        self.driver.find_element_by_css_selector("#profile p a").click()
        WebDriverWait(self.driver, 2).until(EC.url_changes)
        self.assertRegex(self.driver.current_url, "^http://localhost:5000/edit-profile/")

    def update_profile(self):
        self.assertEqual(self.driver.find_element_by_id("bio").text, "")
        self.driver.find_element_by_id("bio").send_keys("Billy's test bio")
        self.driver.find_element_by_css_selector("#editprofile footer button[type='submit']").click()
        WebDriverWait(self.driver, 2).until(EC.url_changes)
        self.assertRegex(self.driver.current_url, "^http://localhost:5000/profile/")
        self.assertEqual(self.driver.find_element_by_css_selector("#profile p").text, "Billy's test bio")

    def test_user_delete(self):
        # 1. to profile
        self.nav_to_login()
        self.login_user()
        self.nav_to_profile()
        # 2. update profile
        self.to_edit_profile()
        self.update_profile()


if __name__ == "__main__":
    unittest.main()
