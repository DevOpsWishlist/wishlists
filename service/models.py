"""
Models for WishLists and Items

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass


######################################################################
#  COMMON  B A S E   M O D E L
######################################################################
class CommonModel():
    """ Base class added persistent methods """

    def create(self):
        """
        Creates a object to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates a object to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a object from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the records in the database """
        logger.info("Processing all records")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a record by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a record by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)


class Item(db.Model, CommonModel):
    """
    Class that represents a Item
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    price = db.Column(db.Numeric(10,2))
    created_time = db.Column(db.DateTime, server_default=db.func.now())
    modified_time = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    wishlist_id = db.Column(db.Integer, db.ForeignKey('wish_list.id'), nullable=False)

    def __repr__(self):
        return f'Item {self.name} id=[{self.id}]'

    def serialize(self):
        """ Serializes a Item into a dictionary """
        return {
            "id": self.id,
            "name": self.name,
            "price": float(self.price),
            "modified_time": self.modified_time,
            "wishlist_id": self.wishlist_id
        }

    def deserialize(self, data):
        """
        Deserializes a Item from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.price = data["price"]
            self.wishlist_id = data["wishlist_id"]
        except KeyError as error:
            raise DataValidationError(
                f'Invalid Item: missing {error.args[0]}'
            )
        except TypeError as error:
            raise DataValidationError(
                'Invalid Item: body of request contained bad or no data'
            )
        return self
   
    def find_by_wishlist_id(self, wishlist_id):
        """ Find a item by its wishlist id """
        logger.info(f'Processing item lookup for wishlist id {wishlist_id} ...')
        return self.query.filter_by(wishlist_id = f'{wishlist_id}').all()

    @classmethod
    def find_by_id(self, id):
        """Returns all item with the given id
        """
        logger.info(f'Processing name query for {id} ...')
        return self.query.filter(self.id == id)

    @classmethod
    def find_by_name(self, name):
        """Returns all item with the given name
        """
        logger.info(f'Processing name query for {name} ...')
        return self.query.filter(self.name == name)

    @classmethod
    def find_by_price(self, price):
        """Returns all item with the given price
        """
        logger.info(f'Processing name query for {price} ...')
        return self.query.filter(self.price == price)

    @classmethod
    def find_by_modified_time(self, modified_time):
        """Returns all item with the given modified_time
        """
        logger.info(f'Processing name query for {modified_time} ...')
        return self.query.filter(self.modified_time == modified_time)

class WishList(db.Model, CommonModel):
    """
    Class that represents a WishList
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    category = db.Column(db.String(63))
    created_time = db.Column(db.DateTime, server_default=db.func.now())
    modified_time = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    items = db.relationship("Item", backref="wish_list", lazy='dynamic')

    def __repr__(self):
        return f'WishList {self.name} id=[{self.id}]'

    def serialize(self):
        """ Serializes a WishList into a dictionary """
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "modified_time": self.modified_time,
        }

    def deserialize(self, data):
        """
        Deserializes a WishList from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.category = data["category"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid WishList: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid WishList: body of request contained bad or no data"
            )
        return self

    @classmethod
    def find_by_id(self, id):
        """Returns all wishlists with the given id
        """
        logger.info(f'Processing name query for {id} ...')
        return self.query.filter(self.id == id)

    @classmethod
    def find_by_name(self, name):
        """Returns all item with the given name
        """
        logger.info(f'Processing name query for {name} ...')
        return self.query.filter(self.name == name)
   
    @classmethod
    def find_by_category(self, category):
        """Returns all item with the given category
        """
        logger.info(f'Processing name query for {category} ...')
        return self.query.filter(self.category == category)
    
    @classmethod
    def find_by_created_time(self, created_time):
        """Returns all item with the given created_time
        """
        logger.info(f'Processing name query for {created_time} ...')
        return self.query.filter(self.created_time == created_time)

    @classmethod
    def find_by_modified_time(self, modified_time):
        """Returns all item with the given modified_time
        """
        logger.info(f'Processing name query for {modified_time} ...')
        return self.query.filter(self.modified_time == modified_time)


        @classmethod
    def find_by_items(self, items):
        """Returns all item with the given items
        """
        logger.info(f'Processing name query for {items} ...')
        return self.query.filter(self.items == items)