"""
<your resource name> API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
import json
from unittest import TestCase
from unittest.mock import MagicMock, patch
from flask_api import status  # HTTP Status Codes
from tests.factories import WishListFactory, ItemFactory
from service.models import WishList, Item, db
from service.routes import app, init_db

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  T E S T   C A S E S
######################################################################
class TestYourResourceServer(TestCase):
    """ WishLists and Items Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
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

######################################################################
#  H E L P E R   M E T H O D S
######################################################################

    def _create_wishlists(self, count):
        """ Factory method to create wishlists in bulk """
        for x in range(count):
            wl = WishList(name=f'wishlist{x}', category=f'cat{x}')
            wl.create()

######################################################################
#  WISHLIST  T E S T   C A S E S
######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
   
    def test_get_wishlist_list(self):
        """ Get a list of WishLists """
        self._create_wishlists(5)
        resp = self.app.get("/wishlists")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data['data']), 5)

    # def test_get_account(self):
    #     """ Get a single Account """
    #     # get the id of an account
    #     account = self._create_accounts(1)[0]
    #     resp = self.app.get(
    #         "/accounts/{}".format(account.id), 
    #         content_type="application/json"
    #     )
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)
    #     data = resp.get_json()
    #     self.assertEqual(data["name"], account.name)

    # def test_get_account_not_found(self):
    #     """ Get an Account that is not found """
    #     resp = self.app.get("/accounts/0")
    #     self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # def test_create_account(self):
    #     """ Create a new Account """
    #     account = AccountFactory()
    #     resp = self.app.post(
    #         "/accounts", 
    #         json=account.serialize(), 
    #         content_type="application/json"
    #     )
    #     self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
    #     # Make sure location header is set
    #     location = resp.headers.get("Location", None)
    #     self.assertIsNotNone(location)
        
    #     # Check the data is correct
    #     new_account = resp.get_json()
    #     self.assertEqual(new_account["name"], account.name, "Names does not match")
    #     self.assertEqual(new_account["addresses"], account.addresses, "Address does not match")
    #     self.assertEqual(new_account["email"], account.email, "Email does not match")
    #     self.assertEqual(new_account["phone_number"], account.phone_number, "Phone does not match")
    #     self.assertEqual(new_account["date_joined"], str(account.date_joined), "Date Joined does not match")

    #     # Check that the location header was correct by getting it
    #     resp = self.app.get(location, content_type="application/json")
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)
    #     new_account = resp.get_json()
    #     self.assertEqual(new_account["name"], account.name, "Names does not match")
    #     self.assertEqual(new_account["addresses"], account.addresses, "Address does not match")
    #     self.assertEqual(new_account["email"], account.email, "Email does not match")
    #     self.assertEqual(new_account["phone_number"], account.phone_number, "Phone does not match")
    #     self.assertEqual(new_account["date_joined"], str(account.date_joined), "Date Joined does not match")

    def test_update_wishlist(self):
        """ Update a Wishlist """
        wl = WishList(name='wishlist', category='cat')
        wl.create()
        update_data = {"name":"wish2","category":"cat"}
        resp = self.app.put(
            "/wishlists/1",
            json=update_data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_wishlist = resp.get_json()
        self.assertEqual(updated_wishlist["name"], "wish2")

    def test_delete_wishlist(self):
        """ Delete a Wishlist """
        wishdata = {"name": "wishname1","category": "category1"}
        wishlist = WishList()
        wishlist.deserialize(wishdata)
        wishlist.create()

        # send delete request
        resp = self.app.delete(
            f'/wishlists/{wishlist.id}',
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    # def test_bad_request(self):
    #     """ Send wrong media type """
    #     account = AccountFactory()
    #     resp = self.app.post(
    #         "/accounts", 
    #         json={"name": "not enough data"}, 
    #         content_type="application/json"
    #     )
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_unsupported_media_type(self):
    #     """ Send wrong media type """
    #     account = AccountFactory()
    #     resp = self.app.post(
    #         "/accounts", 
    #         json=account.serialize(), 
    #         content_type="test/html"
    #     )
    #     self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    # def test_method_not_allowed(self):
    #     """ Make an illegal method call """
    #     resp = self.app.put(
    #         "/accounts", 
    #         json={"not": "today"}, 
    #         content_type="application/json"
    #     )
    #     self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


######################################################################
#  ITEMS   T E S T   C A S E S
######################################################################

    # def test_get_address_list(self):
    #     """ Get a list of Addresses """
    #     # add two addresses to account
    #     account = self._create_accounts(1)[0]
    #     address_list = AddressFactory.create_batch(2)

    #     # Create address 1
    #     resp = self.app.post(
    #         "/accounts/{}/addresses".format(account.id), 
    #         json=address_list[0].serialize(), 
    #         content_type="application/json"
    #     )
    #     self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    #     # Create address 2
    #     resp = self.app.post(
    #         "/accounts/{}/addresses".format(account.id), 
    #         json=address_list[1].serialize(), 
    #         content_type="application/json"
    #     )
    #     self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    #     # get the list back and make sure there are 2
    #     resp = self.app.get(
    #         "/accounts/{}/addresses".format(account.id), 
    #         content_type="application/json"
    #     )
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)

    #     data = resp.get_json()
    #     self.assertEqual(len(data), 2)


    # def test_add_address(self):
    #     """ Add an address to an account """
    #     account = self._create_accounts(1)[0]
    #     address = AddressFactory()
    #     resp = self.app.post(
    #         "/accounts/{}/addresses".format(account.id), 
    #         json=address.serialize(), 
    #         content_type="application/json"
    #     )
    #     self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
    #     data = resp.get_json()
    #     logging.debug(data)
    #     self.assertEqual(data["account_id"], account.id)
    #     self.assertEqual(data["name"], address.name)
    #     self.assertEqual(data["street"], address.street)
    #     self.assertEqual(data["city"], address.city)
    #     self.assertEqual(data["state"], address.state)
    #     self.assertEqual(data["postalcode"], address.postalcode)

    def test_get_items(self):
        """ Get a list of items from a wishlist"""

        # create a known wishlist
        wl = WishList(name='wishlist', category='cat')
        wl.create()
        
        itemdata = {"name": "itemname1","price": 21, "wishlist_id": wl.id}
        item = Item()
        item.deserialize(itemdata)
        item.create()
        
        itemdata_2 = {"name": "itemname2","price": 30, "wishlist_id": wl.id}
        item_2 = Item()
        item_2.deserialize(itemdata_2)
        item_2.create()

        resp = self.app.get(
            f'/wishlists/{wl.id}/items',
            content_type="application/json"
        )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(len(data['data']), 2)

    def test_get_item(self):
        """ Get an item from a wishlist"""

        # create a known wishlist
        wl = WishList(name='wishlist', category='cat')
        wl.create()
        
        itemdata = {"name": "itemname1","price": 21, "wishlist_id": wl.id}
        item = Item()
        item.deserialize(itemdata)
        item.create()

        resp = self.app.get(
            f'/wishlists/{wl.id}/items/{item.id}',
            content_type="application/json"
        )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data['data']['name'], "itemname1")
        self.assertEqual(data['data']['price'], 21)

    def test_create_item(self):
        """ Update a Item """
        wl = WishList(name='wishlist', category='cat')
        wl.create()
        update_data = {"name":"wish2","category":"cat"}

        item_data = {"name":"anyitem1", "price":21, "wishlist_id":wl.id}

        resp = self.app.post(
            '/wishlists/1/items',
            json=item_data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        created_item = resp.get_json()
        self.assertEqual(created_item["name"], "anyitem1")

    def test_update_item(self):
        """ Update a Item """
        wl = WishList(name='wishlist', category='cat')
        wl.create()
        update_data = {"name":"wish2","category":"cat"}

        item = Item(name='anyitem', price=21, wishlist_id=wl.id)
        item.create()
        update_itemdata = {"name":"anyitem1", "price":21, "wishlist_id":wl.id}

        resp = self.app.put(
            f'/wishlists/1/items/{item.id}',
            json=update_itemdata,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_item = resp.get_json()
        self.assertEqual(updated_item["name"], "anyitem1")


    def test_delete_item(self):
        """ Delete an Item """
        wishdata = {"name": "wishname1","category": "category1"}
        wishlist = WishList()
        wishlist.deserialize(wishdata)
        wishlist.create()

        itemdata = {"name": "itemname1","price": 21, "wishlist_id": wishlist.id}
        item = Item()
        item.deserialize(itemdata)
        item.create()

        # send delete request
        resp = self.app.delete(
            f'/wishlists/{wishlist.id}/items/{item.id}',
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
