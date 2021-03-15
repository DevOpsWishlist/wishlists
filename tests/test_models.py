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
        Pet.init_db(app)

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

    
          
