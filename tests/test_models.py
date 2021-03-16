"""
Test cases for WishList and Item Models

"""
import logging
import unittest
import os
from service.models import WishList, Item, DataValidationError, db
from service.routes import app

DATABASE_URI = os.getenv("DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb")

######################################################################
#  Wish   M O D E L   T E S T   C A S E S
######################################################################
class TestWishList(unittest.TestCase):
    """ Test Cases for WishList Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.debug = False #something is wrong here 
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        WishList.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()


    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables


    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_wishlist(self):
        """ Create a wishlist and assert that it exists """
        wishlist = WishList(id=1, name="My List", category="Clothes")  
        self.assertTrue(wishlist != None)
        self.assertEqual(wishlist.id, 1)
        self.assertEqual(wishlist.name, "My List")
    
    def test_add_a_wishlist(self):
        """ Create a wishlist and add it to the database """
        wishlists = WishList.all()
        self.assertEqual(wishlists, [])
        wishlist = WishList(name="My List", category="Clothes")
        self.assertIsNone(wishlist.id)
        wishlist.create()  #at this point, wishlist gets id
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(wishlist.id, 1)
        logging.debug(wishlist)
        wishlists = WishList.all()
        logging.debug(wishlists)
        self.assertEqual(len(wishlists), 1)
          
