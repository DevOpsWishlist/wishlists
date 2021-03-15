"""
Test cases for WishList and Item Models

"""
import logging
import unittest
import os
from service.models import WishList, DataValidationError, db

######################################################################
#  WishList   M O D E L   T E S T   C A S E S
######################################################################
class TestWishList(unittest.TestCase):
    """ Test Cases for WishList Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        pass

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        pass

    def tearDown(self):
        """ This runs after each test """
        pass

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_XXXX(self):
        """ Test something """
        self.assertTrue(True)

    def test_update_a_wishlist(self):
        """ Update a Wishlist """
        wishlist = wishlistFactory()
        logging.debug(wishlist)
        wishlist.create()
        logging.debug(wishlist)
        self.assertEqual(wishlist.name, "FirstWishlist")
        # Change it an save it
        wishlist.name = "FirstWishlist"
        original_id = wishlist.id
        wishlist.save()
        self.assertEqual(wishlist.id, original_id)
        self.assertEqual(wishlist.name, "FirstWishlist")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)
        self.assertEqual(wishlists[0].id, 1)
        self.assertEqual(wishlists[0].name, "FirstWishlist")