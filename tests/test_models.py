import unittest
import os
from service.models import WishList, Item, DataValidationError, db
from service.routes import app, init_db

# DATABASE_URI = os.getenv(
#     "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
# )
from config import DATABASE_URI

######################################################################
#  T E S T   C A S E S
######################################################################
class TestWishLists(unittest.TestCase):
    """ Test Cases for WishLists """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        init_db()

    @classmethod
    def tearDownClass(cls):
        """ Runs once before test suite """
        pass

    def setUp(self):
        """ Runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        """ Runs once after each test case """
        db.session.remove()
        db.drop_all()

    def test_create_a_wishlist(self):
        """ Create a wishlist and assert that it exists """
        wl = WishList(name="wishlist1", category="cat1")
        self.assertTrue(wl != None)
        self.assertEqual(wl.id, None)
        self.assertEqual(wl.name, "wishlist1")
        self.assertEqual(wl.category, "cat1")


    def test_add_a_wishlist(self):
        """ Create a wishlist and add it to the database """
        wls = WishList.all()
        self.assertEqual(wls, [])
        wl = WishList(name="wishlist1", category="cat1")
        self.assertTrue(wl != None)
        self.assertEqual(wl.id, None)
        wl.create()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(wl.id, 1)
        wls = WishList.all()
        self.assertEqual(len(wls), 1)

    def test_update_a_wishlist(self):
        """ Update a WishList """
        wl = WishList(name="wishlist1", category="cat1")
        wl.create()
        self.assertEqual(wl.id, 1)
        # Change it an update it
        wl.category = "hot"
        wl.save()
        self.assertEqual(wl.id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        wls = WishList.all()
        self.assertEqual(len(wls), 1)
        self.assertEqual(wls[0].category, "hot")

    def test_delete_a_wishlist(self):
        """ Delete a WishList """
        wl = WishList(name="wishlist1", category="cat1")
        wl.create()
        self.assertEqual(len(WishList.all()), 1)
        # delete the wishlist and make sure it isn't in the database
        wl.delete()
        self.assertEqual(len(WishList.all()), 0)

    def test_serialize_a_wishlist(self):
        """ Test serialization of a WishList """
        wl = WishList(name="wishlist1", category="cat1")
        data = wl.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], None)
        self.assertIn("name", data)
        self.assertEqual(data["name"], "wishlist1")
        self.assertIn("category", data)
        self.assertEqual(data["category"], "cat1")

    def test_deserialize_a_wishlist(self):
        """ Test deserialization of a WishList """
        data = {"id": 1, "name": "wishlist1", "category": "cat1"}
        wl = WishList()
        wl.deserialize(data)
        self.assertNotEqual(wl, None)
        self.assertEqual(wl.id, None)
        self.assertEqual(wl.name, "wishlist1")
        self.assertEqual(wl.category, "cat1")

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        wl = WishList()
        self.assertRaises(DataValidationError, wl.deserialize, data)

    def test_find_wishlist(self):
        """ Find a WishList by ID """
        wl = WishList(name="wishlist1", category="cat1")
        wl.create()
        foundwish = WishList.find(wl.id)
        self.assertIsNot(foundwish, None)
        self.assertEqual(foundwish.id, wl.id)
        self.assertEqual(foundwish.name, "wishlist1")




class TestItems(unittest.TestCase):
    """ Test Cases for Items """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        init_db()

    @classmethod
    def tearDownClass(cls):
        """ Runs once before test suite """
        pass

    def setUp(self):
        """ Runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        """ Runs once after each test case """
        db.session.remove()
        db.drop_all()

    def test_create_a_item(self):
        """ Create a item and assert that it exists """
        item = Item(name="item1", price=88, wishlist_id=1)
        self.assertTrue(item != None)
        self.assertEqual(item.id, None)
        self.assertEqual(item.name, "item1")
        self.assertEqual(item.price, 88)


    def test_add_a_item(self):
        """ Create a item and add it to the database """
        items = Item.all()
        self.assertEqual(items, [])
        wl = WishList(name="wishlist1", category="cat1")
        item = Item(name="item1", price=88, wishlist_id=1)
        self.assertTrue(item != None)
        self.assertEqual(item.id, None)
        wl.create()
        item.create()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(item.id, 1)
        items = Item.all()
        self.assertEqual(len(items), 1)

    def test_update_a_item(self):
        """ Update a Item """
        wl = WishList(name="wishlist1", category="cat1")
        item = Item(name="item1", price=88, wishlist_id=1)
        wl.create()
        item.create()
        self.assertEqual(item.id, 1)
        # Change it an update it
        item.price = 10
        item.save()
        self.assertEqual(item.id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        items = Item.all()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].price, 10)

    def test_delete_a_item(self):
        """ Delete a Item """
        wl = WishList(name="wishlist1", category="cat1")
        item = Item(name="item1", price=88, wishlist_id=1)
        wl.create()
        item.create()
        self.assertEqual(len(Item.all()), 1)
        # delete the wishlist and make sure it isn't in the database
        item.delete()
        self.assertEqual(len(Item.all()), 0)

    def test_serialize_a_item(self):
        """ Test serialization of a Item """
        item = Item(name="item1", price=88, wishlist_id=1)
        data = item.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], None)
        self.assertIn("name", data)
        self.assertEqual(data["name"], "item1")
        self.assertIn("price", data)
        self.assertEqual(data["price"], 88)

    def test_deserialize_a_item(self):
        """ Test deserialization of a Item """
        data = {"id": 1, "name": "item1", "price": 88, "wishlist_id": 1}
        item = Item()
        item.deserialize(data)
        self.assertNotEqual(item, None)
        self.assertEqual(item.id, None)
        self.assertEqual(item.name, "item1")
        self.assertEqual(item.price, 88)
        self.assertEqual(item.wishlist_id, 1)

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, data)

    def test_find_item(self):
        """ Find a Item by ID """
        wl = WishList(name="wishlist1", category="cat1")
        item = Item(name="item1", price=88, wishlist_id=1)
        wl.create()
        item.create()
        found_item = Item.find(item.id)
        self.assertIsNot(found_item, None)
        self.assertEqual(found_item.id, item.id)
        self.assertEqual(found_item.name, "item1")


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    unittest.main()
