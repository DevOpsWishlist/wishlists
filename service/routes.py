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
from service.models import WishList, Item, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Bullshit!",
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

    app.logger.info("Request to create a wishlist")
    check_content_type("application/json")
    wishlist = WishList()
    wishlist.deserialize(request.get_json())
    wishlist.create()
    message = wishlist.serialize()
    location_url = url_for("list_wishlists", wishlist_id=wishlist.id, _external=True)
    app.logger.info(f'WishList with ID {wishlist.id} created')

    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# DELETE A Wishlist
######################################################################
@app.route("/wishlists/<int:wishlist_id>", methods=["DELETE"])
def delete_wishlists(wishlist_id):
    """
    Delete a Wishlist

    This endpoint will delete a wishlist based the id specified in the path
    """
    app.logger.info(f'Request to delete wishlist with id: {wishlist_id}')
    wishlist = WishList.find(wishlist_id)
    if wishlist:
        wishlist.delete()

    app.logger.info(f'Wishlist with ID [{wishlist_id}] delete complete.')
    return make_response("ITS GONE!", status.HTTP_204_NO_CONTENT)


######################################################################
# DELETE A Item
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items/<int:item_id>", methods=["DELETE"])
def delete_items(wishlist_id, item_id):
    """
    Delete a Item

    This endpoint will delete a item based the id specified in the path
    """
    app.logger.info(f'Request to delete item with id: {item_id}')
    item = Item.find(item_id)
    if item:
        item.delete()

    app.logger.info(f'Item with ID [{item_id}] delete complete.')
    return make_response("ITS GONE!", status.HTTP_204_NO_CONTENT)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    WishList.init_db(app)

def check_content_type(media_type):
    """ Checks that the media type is correct """
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(415, "Content-Type must be {}".format(media_type))
