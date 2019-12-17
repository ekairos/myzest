"""
    *******************
    *     WARNING     *
    *******************

MAKE SURE TO RUN THESE TESTS WITH TEST FLAG IN CLI AS THEY ERASE DB ENTRIES:

'TEST=true python -m unittest tests/unit/test_myzest.py'

or all unit tests :
'TEST=true python -m unittest discover -s tests/unit/'

"""

import unittest
from myzest import mongo, app
from myzest.routes import min_to_hour, oid_date, formdata_to_query, make_query, build_recipe, recipe_to_db,\
    check_file_ext, pic_extensions, update_recipe_views, decrement_session_views
import datetime
from tests.testing_data import fake_author, chocolate_recipe_entry, fake_user, fake_recipe
from bson import ObjectId


class TestMainFunctions(unittest.TestCase):
    """Tests template filters and core functions for MyZest"""

    chocolate_recipe_expected = {
        'author_id': fake_author['_id'],
        'name': 'Chocolate Brownie',
        'description': 'Easy dark chocolate brownie with peanuts',
        'difficulty': 'easy',
        'serves': 8,
        'time': {'total': 50},
        'views': 0,
        'updated': datetime.date.today().isoformat(),
        'ingredients': [{'name': 'dark bitter chocolate', 'amount': '300g'},
                        {'name': 'butter', 'amount': '100g'},
                        {'name': 'white sugar', 'amount': '1 cup'}, {'name': 'eggs', 'amount': '5'},
                        {'name': 'cocoa powder', 'amount': '3/4 cup'},
                        {'name': 'flour', 'amount': '1 cup'}],
        'steps': [{'description': 'Preheat oven to 180C. Line a 20 x 30 cm slice tin or brownie pan.'},
                  {'description': 'Sift the flour and cocoa. Melt the butter and chocolate in a bowl over a saucepan of simmering water. Stir until melted then remove from the heat.'},
                  {'description': 'Beat the eggs and sugar until pale and thick. Add the chocolate and mix until combined.'},
                  {'description': 'Beat the sieved flour mixture into the chocolate. The mixture will be quite thick. Add chopped peanuts.'},
                  {'description': 'Pour into the pan and bake for approximately 30 minutes. The brownie needs to be just cooked.'},
                  {'description': 'The brownie needs to be just cooked. Test with a skewer: it is ready when there are some crumbs still attached to the skewer.'},
                  {'description': 'Leave to cool a little before cutting and serving.'}],
        'foodType': 'dessert'}

    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        self.client.delete()
        mongo.db.users.delete_many({})
        mongo.db.recipes.delete_many({})

    @classmethod
    def tearDownClass(cls):
        mongo.db.users.delete_many({})
        mongo.db.recipes.delete_many({})

    def test_time_filter(self):
        """Tests time filter for recipe duration on recipe and rcp_card templates"""
        self.assertEqual(min_to_hour(45), "45m")
        self.assertEqual(min_to_hour(60), "1h")
        self.assertEqual(min_to_hour(70), "1h10")
        self.assertEqual(min_to_hour(16.04), "16m")
        self.assertEqual(min_to_hour(136.04), "2h16")
        self.assertEqual(min_to_hour("25"), "error")
        self.assertEqual(min_to_hour("two hours"), "error")
        self.assertEqual(min_to_hour(False), "error")
        self.assertEqual(min_to_hour(True), "error")

    def test_oid_date_filter(self):
        """Tests the time stamp from ObjectId is converted into date format - profile template"""
        mongo.db.users.insert_one({'username': 'fake'})
        user_document = mongo.db.users.find_one({'username': 'fake'})
        self.assertEqual(oid_date(user_document['_id']), datetime.date.today())

    def test_formdata_to_query(self):
        """The data from the search form should be cleaned and builds a proper query string for mongoDB"""

        default_query_output = {'serves': {'$gte': 1, '$lte': 20}, 'time.total': {'$gte': 5, '$lte': 240}}

        self.assertEqual(formdata_to_query({}), default_query_output)

        self.assertEqual(formdata_to_query({"difficulty": "any"}), default_query_output)
        self.assertEqual(formdata_to_query({"difficulty": ""}), default_query_output)
        self.assertNotRegex(str(formdata_to_query({"difficulty": "dessert"})), "'difficulty': 'main'")
        self.assertNotIn('difficulty', formdata_to_query({"difficulty": "dessert"}))
        self.assertEqual('easy', formdata_to_query({"difficulty": "easy"})['difficulty'])

        self.assertEqual(formdata_to_query({"foodType": "any"}), default_query_output)
        self.assertEqual(formdata_to_query({"foodType": ""}), default_query_output)
        self.assertEqual(formdata_to_query({"foodType": "something"}), default_query_output)
        self.assertNotIn('foodType', formdata_to_query({"foodType": "something"}))
        self.assertIn('foodType', formdata_to_query({"foodType": "main"}))
        self.assertEqual('main', formdata_to_query({"foodType": "main"})['foodType'])

        self.assertEqual(formdata_to_query({"textSearch": ""}), default_query_output)
        self.assertRegex(str(formdata_to_query({"textSearch": "word"})), "'\$text': {'\$search': 'word'}}")

        query = formdata_to_query({'timer.start': 35, 'timer.stop': 240})
        self.assertEqual(query['time.total'], {'$gte': 35, '$lte': 240})
        query = formdata_to_query({'timer.start': '35', 'timer.stop': '240'})
        self.assertEqual(query['time.total'], {'$gte': 35, '$lte': 240})

        query = formdata_to_query({'serve.start': 5, 'serve.stop': 10})
        self.assertEqual(query['serves'], {'$gte': 5, '$lte': 10})
        query = formdata_to_query({'serve.start': '5', 'serve.stop': '10'})
        self.assertEqual(query['serves'], {'$gte': 5, '$lte': 10})

        query = formdata_to_query({"difficulty": "easy", "textSearch": "fish", "foodType": "dessert"})
        self.assertRegex(str(query), "'difficulty': 'easy'")
        self.assertRegex(str(query), "'foodType': 'dessert'")
        self.assertRegex(str(query), "'\$text': {'\$search': 'fish'}}")
        self.assertRegex(str(query), "'time.total': {'\$gte': 5, '\$lte': 240}")
        self.assertRegex(str(query), "'serves': {'\$gte': 1, '\$lte': 20}")

        query = formdata_to_query({"difficulty": "average", "textSearch": "chocolate", "foodType": "sauce",
                                   'timer.start': 50, 'timer.stop': 100, 'serve.start': '5', 'serve.stop': '10'})
        self.assertRegex(str(query), "'difficulty': 'average'")
        self.assertRegex(str(query), "'foodType': 'sauce'")
        self.assertRegex(str(query), "'\$text': {'\$search': 'chocolate'}}")
        self.assertRegex(str(query), "'time.total': {'\$gte': 50, '\$lte': 100}")
        self.assertRegex(str(query), "'serves': {'\$gte': 5, '\$lte': 10}")

    def test_make_query(self):
        """Should return string to query mongoDB and sorting criteria as tuple"""
        default_query_output = {'serves': {'$gte': 1, '$lte': 20}, 'time.total': {'$gte': 5, '$lte': 240}}
        # with no query given
        self.assertEqual(make_query({'sort': "favorite"}), (default_query_output, {'favorite': -1}))
        self.assertEqual(make_query({'sort': "views"}), (default_query_output, {'views': -1}))
        self.assertEqual(make_query({'sort': "updated"}), (default_query_output, {'updated': -1}))
        self.assertEqual(make_query({'sort': "time.total"}), (default_query_output, {'time.total': 1}))
        self.assertEqual(make_query({'sort': "serves"}), (default_query_output, {'serves': 1}))
        self.assertEqual(make_query({'sort': "name"}), (default_query_output, {'name': 1}))
        # Given filter criteria
        new_query = make_query({"difficulty": "easy", "foodType": "dessert", 'timer.start': 50,
                                'timer.stop': 100, 'serve.start': '5', 'serve.stop': '10', 'sort': "name"})
        self.assertTrue(type(new_query), tuple)
        self.assertEqual(new_query,
                         ({"difficulty": "easy", "foodType": "dessert",
                           'serves': {'$gte': 5, '$lte': 10}, 'time.total': {'$gte': 50, '$lte': 100}},
                          {'name': 1}))

    def test_check_file_ext(self):
        """Should return False if no file or wrong file extension"""
        self.assertTrue(check_file_ext("correctfile.gif", pic_extensions))
        self.assertTrue(check_file_ext("correctfile.jpeg", pic_extensions))
        self.assertTrue(check_file_ext("correctfile.jpg", pic_extensions))
        self.assertTrue(check_file_ext("correctfile.png", pic_extensions))

        self.assertFalse(check_file_ext("wrongfile.pn", pic_extensions))
        self.assertFalse(check_file_ext("wrongfile.jpe", pic_extensions))
        self.assertFalse(check_file_ext("wrongfile.fig", pic_extensions))
        self.assertFalse(check_file_ext("wrongfile.mp3", pic_extensions))
        self.assertFalse(check_file_ext("wrongfile.pdf", pic_extensions))

        self.assertFalse(check_file_ext("", pic_extensions))

    def test_upload_recipe(self):
        """User adding and editing recipe main functions: build_recipe and recipe_to_db
        check_file_extension is tested separately above.
        1. build recipe dictionary from form data
        2. insert recipe into database and update author's recipe's list
        """
        with self.client:
            mongo.db.users.insert_one(fake_author)
            mongo.db.users.insert_one(fake_user)
            # 1.
            recipe = build_recipe(author_id=fake_author['_id'], data=chocolate_recipe_entry)
            self.maxDiff = None
            self.assertEqual(type(recipe), dict)
            self.assertEqual(recipe, self.chocolate_recipe_expected)
            # 2.
            recipe_inserted = recipe_to_db(author_id=fake_author['_id'], recipe=recipe)
            recipe_in_db = mongo.db.recipes.find_one(recipe)
            self.assertEqual(recipe_inserted, recipe_in_db['_id'])
            lily = mongo.db.users.find_one({'_id': fake_user['_id']})
            self.assertNotIn(recipe_inserted, lily['recipes'])
            george = mongo.db.users.find_one({'_id': fake_author['_id']})
            self.assertIn(recipe_inserted, george['recipes'])

    def test_update_view(self):
        """DB recipe with given _id should have its 'views' field incremented or decremented by one
        update_view is called when user visits a recipe's page and by decrement_session_views function"""
        mongo.db.recipes.insert_one(fake_recipe)
        sushis = mongo.db.recipes.find_one({})
        self.assertEqual(sushis['views'], 1)

        update_recipe_views(sushis['_id'], 1)
        sushis = mongo.db.recipes.find_one({})
        self.assertEqual(sushis['views'], 2)

        update_recipe_views(sushis['_id'], -1)
        sushis = mongo.db.recipes.find_one({})
        self.assertEqual(sushis['views'], 1)

    def test_decrement_session_views(self):
        """Tests a recipe's 'views' field is decremented if the author logs in after viewing the recipe page"""
        mongo.db.recipes.insert_one(fake_recipe)
        sushis = mongo.db.recipes.find_one({})
        self.assertEqual(sushis['views'], 1)

        decrement_session_views(fake_author['recipes'], [fake_recipe['_id']])
        sushis = mongo.db.recipes.find_one({})
        self.assertEqual(sushis['views'], 0)

    def test_no_decrement_views(self):
        """Tests the recipe's views is not decremented when another user than recipe's author logs in
        after viewing the recipe"""
        mongo.db.recipes.insert_one(fake_recipe)
        sushis = mongo.db.recipes.find_one({})
        self.assertEqual(sushis['views'], 1)

        update_recipe_views(sushis['_id'], 1)
        decrement_session_views([fake_user['recipes']], [sushis['_id']])
        sushis = mongo.db.recipes.find_one({})
        self.assertEqual(sushis['views'], 2)


if __name__ == '__main__':
    unittest.main()
