"""
TestWishList API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from flask_api import status  # HTTP Status Codes
from service.models import db, WishList, Item #import wishlist object
from service.routes import app, init_db

DATABASE_URI = os.getenv("DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb")

######################################################################
#  T E S T   C A S E S
######################################################################
class TestWishListServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.debug = False
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
        self.app = app.test_client() #not sure the purpose of this 

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################
    
    def test_create_a_wishlist(self):
        """ Create a wishlist and assert that it exists """
        wishlist = WishList(id=1, name="My List", category="Clothes")  
        self.assertTrue(wishlist != None)
        self.assertEqual(wishlist.id, 1)
        self.assertEqual(wishlist.name, "My List")
        self.assertEqual(wishlist.category, "Clothes")
        #self.assertEqual(wishlist.available, True)

        
    def test_get_wishlist_list(self):
        """ Get a list of wishlists """
        wishlist = WishList(id=1, name="My List", category="Clothes")
        wishlist.create() 
        wishlist = WishList(id=2, name="Your List", category="Clothes")
        wishlist.create() 
        resp = self.app.get("/wishlists")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 2)
        
    

