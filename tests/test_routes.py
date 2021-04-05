"""
WishLists API Service Test Suite

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
from urllib.parse import quote_plus

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
        wishlists = [] #added list to append to 
        for x in range(count):
            wl = WishList(name=f'wishlist{x}', category=f'cat{x}')
            wl.create()
            wishlists.append(wl)
        return wishlists
    
    def _create_items(self, count):
        """ Factory method to create items in bulk """
        wl = WishList(name = 'wishlist1', category = 'category1')
        wl.create()

        items = []
        for x in range(count):
            cost = 1+x 
            item = Item(name=f'item{x}', price=cost, wishlist_id = 1) #should this be a changing number?
            item.create() 
            items.append(item)
        
        return items

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

    def test_get_wishlist(self):
        """ Get a wishlist by id """

        # create a known wishlist
        wl = WishList(name='wishlist', category='cat')
        wl.create()

        resp = self.app.get(
            f'/wishlists/{wl.id}',
            content_type="application/json"
        )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data['data']['name'], 'wishlist')
        self.assertEqual(data['data']['category'], 'cat')
        self.assertEqual(data['data']['id'], 1)

    def test_create_wishlist(self):
        """ Create a WishList """
        wish_data = {"name":"wish2","category":"cat"}

        resp = self.app.post(
            '/wishlists',
            json=wish_data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        created_wishlist = resp.get_json()
        self.assertEqual(created_wishlist["name"], "wish2")

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


    def test_unsupported_media_type(self):
        """ Send wrong media type """
        resp = self.app.post(
            "/wishlists", 
            json={}, 
            content_type="test/html"
        )
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_method_not_allowed(self):
        """ Make an illegal method call """
        resp = self.app.put(
            "/wishlists", 
            json={"not": "today"}, 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_query_wishlists_by_name(self):
        """ Query Wishlists by Name """
        wl = self._create_wishlists(10)
        test_name = wl[0].name
        wl_name = [wish for wish in wl if wish.name == test_name]

        #API Call 
        resp = self.app.get(
            f'/wishlists?name={test_name}'
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json() #dict
        logging.debug('data = %s', data)
        name_data = data["data"] #dict w/ list as value
        self.assertEqual(len(name_data), len(wl_name))
        
        for wishlist in name_data:
            logging.debug('wishlist = %s', wishlist)
            self.assertEqual(name_data[0]["name"], test_name)

    def test_query_wishlists_by_category(self):
        """ Query Wishlists by Category """
        wl = self._create_wishlists(10)
        test_category = wl[0].category
        wl_category = [wish for wish in wl if wish.category == test_category]

        #API Call 
        resp = self.app.get(
            f'/wishlists?category={test_category}'
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json() #dict
        logging.debug('data = %s', data)
        category_data = data["data"] #dict w/ list as value
        self.assertEqual(len(category_data), len(wl_category))
        
        for wishlist in category_data:
            logging.debug('wishlist = %s', wishlist)
            self.assertEqual(wishlist["category"], test_category)

######################################################################
#  I T E M S   T E S T   C A S E S
######################################################################

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
        self.assertEqual(data['data']['name'], "itemname1")
        self.assertEqual(data['data']['price'], 21)

    def test_create_item(self):
        """ Create a Item """
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

    def test_query_items_by_name(self):
        """ Query Items by Name """
        items = self._create_items(10)
        test_name = items[0].name
        wl_id = items[0].wishlist_id
        item_name = [item for item in items if item.name == test_name]
        
        #API Call 
        resp = self.app.get(
            f'/wishlists/{wl_id}/items?name={test_name}'
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.assertIn(b'item0', resp.data)
        self.assertNotIn(b'NotAnItem', resp.data)
        
        data = resp.get_json() #dict
        logging.debug('data = %s', data)
        name_data = data["data"] #dict w/ list as value
        
        for item in name_data:
            logging.debug('item = %s', item)
            self.assertEqual(item["name"], test_name)

    def test_query_items_by_price(self):
        """ Query Items by Price """
        items = self._create_items(10)
        test_price = items[0].price
        wl_id = items[0].wishlist_id
        item_price = [item for item in items if item.price == test_price]
        
        #API Call 
        resp = self.app.get(
            f'/wishlists/{wl_id}/items?price={test_price}'
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json() #dict
        logging.debug('data = %s', data)
        price_data = data["data"] #dict w/ list as value
        
        for item in price_data:
            logging.debug('item = %s', item)
            self.assertEqual(item["price"], test_price) 

    

    