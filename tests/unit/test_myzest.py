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
from myzest import mongo
from myzest.routes import min_to_hour, oid_date, formdata_to_query, make_query
import datetime


class TestMainFunctions(unittest.TestCase):
    """Tests template filters and core functions for MyZest"""

    @classmethod
    def tearDownClass(cls):
        mongo.db.users.delete_many({'username': 'fake'})

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


if __name__ == '__main__':
    unittest.main()