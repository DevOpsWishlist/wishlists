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
            "price": self.category,
            "modified_time": self.modified_time,
            "wishlist_id": self.wishlist_id
        }

    def create(self):
        """
        Creates a Item to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates a Item to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a Item from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    # def deserialize(self, data):
    #     """
    #     Deserializes a Item from a dictionary

    #     Args:
    #         data (dict): A dictionary containing the resource data
    #     """
    #     try:
    #         self.name = data["name"]
    #     except KeyError as error:
    #         raise DataValidationError(
    #             "Invalid Item: missing " + error.args[0]
    #         )
    #     except TypeError as error:
    #         raise DataValidationError(
    #             "Invalid Item: body of request contained bad or no data"
    #         )
    #     return self



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

    def create(self):
        """
        Creates a WishList to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates a WishList to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a WishList from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

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
