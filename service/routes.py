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
        "Hello World!",
        status.HTTP_200_OK,
	)

######################################################################
# GET HTML HOMEPAGE
######################################################################
@app.route('/home')
def home():
    return app.send_static_file('index.html')

######################################################################
# LIST ALL WishLists
######################################################################
@app.route("/wishlists", methods=["GET"])
def list_wishlists():
    """ Returns all of the Wishlists """
    app.logger.info("Request for wishlists")
    
    wishlists = []
    category = request.args.get("category")
    name = request.args.get("name")

    if category:
        wishlists = WishList.find_by_category(category)
    elif name:
        wishlists = WishList.find_by_name(name)
    else:
        wishlists = WishList.all()
   # wishlists = WishList.all()
   
    results = [wishlist.serialize() for wishlist in wishlists]
    app.logger.info(f'Returning {len(results)}')
    
    response_body = {
    	'data': results,
    	'count': len(results)
    }
    return make_response(jsonify(response_body), status.HTTP_200_OK)

######################################################################
# READ an individual wishlist
######################################################################
@app.route("/wishlists/<int:wishlist_id>", methods=["GET"])
def get_wishlist(wishlist_id):

    """ Returns a wishlist by id """
    app.logger.info('Request for an wishlist')
    wl = WishList()
    found_wl = wl.find(wishlist_id)
    found_wl_serialized = found_wl.serialize()
    found_wl_id = str(found_wl_serialized['id'])
    app.logger.info(f'Returning item: {found_wl_id}')
    response_body = {
        'data': found_wl_serialized,
        'id': found_wl_id
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
    wishlist = WishList.find(wishlist_id)
    if not wishlist:
        raise NotFound("Wishlist with id '{}' was not found.".format(wishlist_id))

    wishlist.deserialize(request.get_json())
    wishlist.id = wishlist_id
    wishlist.save()
    return make_response(jsonify(wishlist.serialize()), status.HTTP_200_OK)


##################################################################################################################################################################################################################
##################################################################################################################################################################################################################


######################################################################
# LIST items belonging to a wishlist
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items", methods=["GET"])
def get_items(wishlist_id):

    """ Returns all of the items in a wishlist """
    app.logger.info('Request for items in wishlist')
    #item = Item()
    items = []

    name = request.args.get("name")
    price = request.args.get("price")

    if name: 
        items = Item.find_by_name(name)
    elif price: 
        items = Item.find_by_price(price)
    else: 
        items = Item.all()

    #items = item.find_by_wishlist_id(wishlist_id)
    results = [item.serialize() for item in items] 
    
    app.logger.info(f'Returning {len(results)} items')
    response_body = {
    	'data': results,
    	'count': len(results)
    }
    return make_response(jsonify(response_body), status.HTTP_200_OK)

######################################################################
# READ an individual item belonging to a wishlist
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items/<int:item_id>", methods=["GET"])
def get_item(wishlist_id, item_id):

    """ Returns one item in a wishlist """
    app.logger.info('Request for an item in wishlist')
    item = Item()
    found_item = item.find(item_id)
    found_item_serialized = found_item.serialize()
    found_item_id = str(found_item_serialized['id'])
    app.logger.info(f'Returning item: {found_item_id}')
    response_body = {
    	'data': found_item_serialized,
    	'id': found_item_id
    }
    return make_response(jsonify(response_body), status.HTTP_200_OK)


######################################################################
# DELETE AN Item
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
# UPDATE AN EXISTING Item
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items/<int:item_id>", methods=["PUT"])
def update_items(wishlist_id, item_id):
    """
    Update an Item

    This endpoint will update an item based the body that is posted
    """
    app.logger.info("Request to update item with id: %s", item_id)
    check_content_type("application/json")
    item = Item.find(item_id)
    if not item:
        raise NotFound("Item with id '{}' was not found.".format(item_id))
    item.deserialize(request.get_json())
    item.id = item_id
    item.save()
    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)

######################################################################
# CREATE A Item
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items", methods=["POST"])
def create_item(wishlist_id):
    """ Creates an item in a wishlist  """

    app.logger.info("Request to create an item in a wishlist")
    check_content_type("application/json")
    item = Item()
    item.deserialize(request.get_json())
    item.create()
    message = item.serialize()
    location_url = url_for("get_item", wishlist_id=item.wishlist_id, item_id=item.id, _external=True)
    app.logger.info(f'Item with ID {item.id} created')

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

def check_content_type(media_type):
    """ Checks that the media type is correct """
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(415, "Content-Type must be {}".format(media_type))
