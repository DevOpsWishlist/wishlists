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