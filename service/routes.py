"""
Shopcart Service

This microservice handles the lifecycle of Shopcarts
"""
from . import app  # Import Flask application

from flask import jsonify, request, url_for, make_response, abort
from service.models import Shopcart, Item
from service.common import status  # HTTP Status Codes

######################################################################
# S H O P C A R T   M E T H O D S
######################################################################


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    return jsonify(
        name="Shopcart REST API Service",
        version="1.0",
        paths=url_for("list_shopcarts", _external=True),
    ), status.HTTP_200_OK

######################################################################
# LIST ALL SHOPCARTS
######################################################################


@app.route("/shopcarts", methods=["GET"])
def list_shopcarts():
    """Returns all of the Shopcarts"""
    app.logger.info("Request for Shopcart list")
    shopcarts = []

    # Process the query string if any
    name = request.args.get("name")
    if name:
        shopcarts = Shopcart.find_by_name(name)
    else:
        shopcarts = Shopcart.all()

    # Return as an array of dictionaries
    results = [shopcart.serialize() for shopcart in shopcarts]

    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# CREATE A NEW SHOPCART
######################################################################


@app.route("/shopcarts", methods=["POST"])
def create_shopcarts():
    """
    Creates a Shopcart
    This endpoint will create an Shopcart based the data in the body that is posted
    """
    app.logger.info("Request to create an Shopcart")
    check_content_type("application/json")

    # Create the shopcart
    shopcart = Shopcart()
    shopcart.deserialize(request.get_json())
    shopcart.create()

    # Create a message to return
    message = shopcart.serialize()
    location_url = url_for("create_shopcarts", shopcart_id=shopcart.id, _external=True)

    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# RETRIEVE A SHOPCART
######################################################################


@app.route("/shopcarts/<int:shopcart_id>", methods=["GET"])
def get_shopcarts(shopcart_id):
    """
    Retrieve a single Shopcart

    This endpoint will return an Shopcart based on it's id
    """
    app.logger.info("Request for Shopcart with id: %s", shopcart_id)

    # See if the shopcart exists and abort if it doesn't
    shopcart = Shopcart.find(shopcart_id)
    if not shopcart:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Shopcart with id '{shopcart_id}' could not be found.",
        )

    return make_response(jsonify(shopcart.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A SHOPCART
######################################################################
@app.route("/shopcarts/<int:shopcart_id>", methods=["DELETE"])
def delete_shopcarts(shopcart_id):
    """
    Delete an Shopcart

    This endpoint will delete an Shopcart based the id specified in the path
    """
    app.logger.info("Request to delete shopcart with id: %s", shopcart_id)

    # Retrieve the shopcart to delete and delete it if it exists
    shopcart = Shopcart.find(shopcart_id)
    if shopcart:
        shopcart.delete()

    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
# UPDATE AN EXISTING SHOPCART
######################################################################
@app.route("/shopcarts/<int:shopcart_id>", methods=["PUT"])
def update_shopcarts(shopcart_id):
    """
    Update an Shopcart

    This endpoint will update a Shopcart based the body that is posted
    """
    app.logger.info("Request to update shopcart with id: %s", shopcart_id)
    check_content_type("application/json")

    # See if the shopcart exists and abort if it doesn't
    shopcart = Shopcart.find(shopcart_id)
    if not shopcart:
        abort(
            status.HTTP_404_NOT_FOUND, f"Shopcart with id '{shopcart_id}' was not found."
        )

    # Update from the json in the body of the request
    shopcart.deserialize(request.get_json())
    shopcart.id = shopcart_id
    shopcart.update()

    return make_response(jsonify(shopcart.serialize()), status.HTTP_200_OK)


######################################################################
# I T E M   M E T H O D S
######################################################################

######################################################################
# ADD AN ITEM TO A SHOPCART
######################################################################
@app.route("/shopcarts/<int:shopcart_id>/items", methods=["POST"])
def create_items(shopcart_id):
    """
    Create an Item on an Shopcart

    This endpoint will add an item to an shopcart
    """
    app.logger.info("Request to create an Item for Shopcart with id: %s", shopcart_id)
    check_content_type("application/json")

    # See if the shopcart exists and abort if it doesn't
    shopcart = Shopcart.find(shopcart_id)
    if not shopcart:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Shopcart with id '{shopcart_id}' could not be found.",
        )

    # Create an item from the json data
    item = Item()
    item.deserialize(request.get_json())

    # Append the item to the shopcart
    shopcart.items.append(item)
    shopcart.update()

    # Prepare a message to return
    message = item.serialize()

    return make_response(jsonify(message), status.HTTP_201_CREATED)

######################################################################
# RETRIEVE AN ITEM FROM A SHOPCART
######################################################################


@app.route("/shopcarts/<int:shopcart_id>/items/<int:item_id>", methods=["GET"])
def get_items(shopcart_id, item_id):
    """
    Get a Shopcart

    This endpoint returns just an item
    """
    app.logger.info(
        "Request to retrieve Item %s for Shopcart id: %s", (item_id, shopcart_id)
    )

    # See if the item exists and abort if it doesn't
    item = Item.find(item_id)
    if not item:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Shopcart with id '{item_id}' could not be found.",
        )

    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)


######################################################################
# LIST ITEMS
######################################################################
@app.route("/shopcarts/<int:shopcart_id>/items", methods=["GET"])
def list_items(shopcart_id):
    """Returns all of the Items for an Shopcart"""
    app.logger.info("Request for all Items for Shopcart with id: %s", shopcart_id)

    # See if the shopcart exists and abort if it doesn't
    shopcart = Shopcart.find(shopcart_id)
    if not shopcart:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Shopcart with id '{shopcart_id}' could not be found.",
        )

    # Get the items for the shopcart
    results = [item.serialize() for item in shopcart.items]

    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# UPDATE AN ITEM
######################################################################
@app.route("/shopcarts/<int:shopcart_id>/items/<int:item_id>", methods=["PUT"])
def update_items(shopcart_id, item_id):
    """
    Update an Item
    This endpoint will update an item based the body that is posted
    """
    app.logger.info(
        "Request to update Item %s for Shopcart id: %s", (item_id, shopcart_id)
    )
    check_content_type("application/json")

    # See if the item exists and abort if it doesn't
    item = Item.find(item_id)
    if not item:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Shopcart with id '{item_id}' could not be found.",
        )

    # Update from the json in the body of the request
    item.deserialize(request.get_json())
    item.id = item_id
    item.update()

    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE AN ITEM
######################################################################
@app.route("/shopcarts/<int:shopcart_id>/items/<int:item_id>", methods=["DELETE"])
def delete_items(shopcart_id, item_id):
    """
    Delete an Item

    This endpoint will delete an Item based the id specified in the path
    """
    app.logger.info(
        "Request to delete Item %s for Shopcart id: %s", (item_id, shopcart_id)
    )

    # See if the item exists and delete it if it does
    item = Item.find(item_id)
    if item:
        item.delete()

    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
# U T I L I T Y   F U N C T I O N S
######################################################################

def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
