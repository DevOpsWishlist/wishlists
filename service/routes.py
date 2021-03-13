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
    """ Returns all of the Pets """
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
# CREATE/ADD A WISHLIST
######################################################################
@app.route("/wishlists", methods=["POST"]) #not sure about the method yet 
def create_wishlists():
    """
    Creates a wishlist
    This endpoint will create a wishlist based the data in the body that is posted
    """
    app.logger.info("Request to create a wishlist")
    check_content_type("application/json")
    wishlists = WishList() 
    wishlists.deserialize(request.get_json())
    wishlists.create()
    message = wishlists.serialize()
    location_url = url_for("get_wishlists", wishlists_id=wishlists.id, _external=True) 

    app.logger.info("Wishlist with ID [%s] created.", pet.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    WishList.init_db(app)
