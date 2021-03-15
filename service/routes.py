"""
My Service

Describe what your service does here
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import WishList, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Bullshit",
        status.HTTP_200_OK,
	)

######################################################################
# LIST ALL WishLists
######################################################################
@app.route("/wishlists", methods=["GET"])
def list_wishlists():
    """ Returns all of the Wishlists """
    app.logger.info("Request for wishlists")
    wishlists = WishList.all()
    results = [wishlist.serialize() for wishlist in wishlists]
    app.logger.info(f'Returning {len(results)}')
    response_body = {
    	'data': results,
    	'count': len(results)
    }
    return make_response(jsonify(response_body), status.HTTP_200_OK)


######################################################################
# CREATE A WishList
######################################################################
@app.route("/wishlists", methods=["POST"])
def create_wishlists():
    """ Creates a wishlist  """


######################################################################
# UPDATE AN EXISTING Wishlist
######################################################################
@app.route("/wishlists/<int:wishlist_id>", methods=["PUT"])
def update_wishlists(wishlist_id):
    """
    Update a Wishlist
    This endpoint will update a Wishlist based the body that is posted
    """
    app.logger.info("Request to update wishlist with id: %s", wishlist_id)
    check_content_type("application/json")
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        raise NotFound("Wishlist with id '{}' was not found.".format(wishlist_id))
    wishlist.deserialize(request.get_json())
    wishlist.id = wishlist_id
    wishlist.save()
    return make_response(jsonify(wishlist.serialize()), status.HTTP_200_OK)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    WishList.init_db(app)
