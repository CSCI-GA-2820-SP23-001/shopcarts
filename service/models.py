"""
Models for Shopcart

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from abc import abstractmethod

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


# Function to initialize the database
def init_db(app):
    """ Initializes the SQLAlchemy app """
    Shopcart.init_db(app)

######################################################################
#  P E R S I S T E N T   B A S E   M O D E L
######################################################################


class PersistentBase:
    """Base class added persistent methods"""

    def __init__(self):
        self.id = None  # pylint: disable=invalid-name

    @abstractmethod
    def serialize(self) -> dict:
        """Convert an object into a dictionary"""

    @abstractmethod
    def deserialize(self, data: dict) -> None:
        """Convert a dictionary into an object"""

    def create(self):
        """
        Creates a Shopcart to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Shopcart to the database
        """
        logger.info("Updating %s", self.name)
        db.session.commit()

    def delete(self):
        """Removes a Shopcart from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """Returns all of the records in the database"""
        logger.info("Processing all records")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a record by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

######################################################################
#  I T E M   M O D E L
######################################################################


class Item(db.Model, PersistentBase):
    """
    Class that represents an Item
    """

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    shopcart_id = db.Column(db.Integer, db.ForeignKey("shopcart.id", ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(64))  # e.g., work, home, vacation, etc.
    quantity = db.Column(db.String(4))
    color = db.Column(db.String(20))
    size = db.Column(db.String(2))
    price = db.Column(db.String(6))

    def __repr__(self):
        return f"<Item {self.name} id=[{self.id}] shopcart[{self.shopcart_id}]>"

    def __str__(self):
        return f"{self.name}: {self.quantity}, {self.color}, {self.size} {self.price}"

    def serialize(self) -> dict:
        """Converts an Item into a dictionary"""
        return {
            "id": self.id,
            "shopcart_id": self.shopcart_id,
            "name": self.name,
            "quantity": self.quantity,
            "color": self.color,
            "size": self.size,
            "price": self.price
        }

    def deserialize(self, data: dict) -> None:
        """
        Populates an Item from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.shopcart_id = data["shopcart_id"]
            self.name = data["name"]
            self.quantity = data["quantity"]
            self.color = data["color"]
            self.size = data["size"]
            self.price = data["price"]
        except KeyError as error:
            raise DataValidationError("Invalid Item: missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Item: body of request contained "
                "bad or no data " + error.args[0]
            ) from error
        return self


######################################################################
#  S H O P C A R T   M O D E L
######################################################################


class Shopcart(db.Model, PersistentBase):
    """
    Class that represents a Shopcart
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    phone_number = db.Column(db.String(32), nullable=True)  # phone number is optional
    date_joined = db.Column(db.Date(), nullable=False, default=date.today())
    items = db.relationship("Item", backref="shopcart", passive_deletes=True)

    def __repr__(self):
        return f"<Shopcart {self.name} id=[{self.id}]>"

    def serialize(self):
        """Converts a Shopcart into a dictionary"""
        shopcart = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "date_joined": self.date_joined.isoformat(),
            "items": [],
        }
        for item in self.items:
            shopcart["items"].append(item.serialize())
        return shopcart

    def deserialize(self, data):
        """
        Populates a Shopcart from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.email = data["email"]
            self.phone_number = data.get("phone_number")
            self.date_joined = date.fromisoformat(data["date_joined"])
            # handle inner list of items
            item_list = data.get("items")
            for json_item in item_list:
                item = Item()
                item.deserialize(json_item)
                self.items.append(item)
        except KeyError as error:
            raise DataValidationError("Invalid Shopcart: missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Shopcart: body of request contained "
                "bad or no data - " + error.args[0]
            ) from error
        return self

    @classmethod
    def find_by_name(cls, name):
        """Returns all Shopcarts with the given name

        Args:
            name (string): the name of the Shopcarts you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
