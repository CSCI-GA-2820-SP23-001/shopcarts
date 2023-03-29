"""
Test cases for Shopcart Model

"""
import logging
import unittest
import os
from service import app
from service.models import Shopcart, Item, DataValidationError, db
from tests.factories import ShopcartFactory, ItemFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  S H O P C A R T   M O D E L   T E S T   C A S E S
######################################################################

class TestShopcart(unittest.TestCase):
    """Test Cases for Shopcart Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Shopcart.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""

    def setUp(self):
        """This runs before each test"""
        db.session.query(Shopcart).delete()  # clean up the last tests
        db.session.query(Item).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  S H O P C A R T    T E S T   C A S E S   H E R E
    ######################################################################

    def test_create_a_shopcart(self):
        """It should Create a Shopcart and assert that it exists"""
        fake_shopcart = ShopcartFactory()
        # pylint: disable=unexpected-keyword-arg
        shopcart = Shopcart(
            name=fake_shopcart.name,
            email=fake_shopcart.email,
            phone_number=fake_shopcart.phone_number,
            date_joined=fake_shopcart.date_joined,
        )
        self.assertIsNotNone(shopcart)
        self.assertEqual(shopcart.id, None)
        self.assertEqual(shopcart.name, fake_shopcart.name)
        self.assertEqual(shopcart.email, fake_shopcart.email)
        self.assertEqual(shopcart.phone_number, fake_shopcart.phone_number)
        self.assertEqual(shopcart.date_joined, fake_shopcart.date_joined)

    def test_list_all_shopcarts(self):
        """It should List all Shopcarts in the database"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        for shopcart in ShopcartFactory.create_batch(5):
            shopcart.create()
        # Assert that there are not 5 shopcarts in the database
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 5)

    def test_read_shopcart(self):
        """It should Read an shopcart"""
        shopcart = ShopcartFactory()
        shopcart.create()

        # Read it back
        found_shopcart = Shopcart.find(shopcart.id)
        self.assertEqual(found_shopcart.id, shopcart.id)
        self.assertEqual(found_shopcart.name, shopcart.name)
        self.assertEqual(found_shopcart.email, shopcart.email)
        self.assertEqual(found_shopcart.phone_number, shopcart.phone_number)
        self.assertEqual(found_shopcart.date_joined, shopcart.date_joined)
        self.assertEqual(found_shopcart.items, [])

    def test_update_shopcart(self):
        """It should Update a shopcart"""
        shopcart = ShopcartFactory(email="advent@change.me")
        shopcart.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(shopcart.id)
        self.assertEqual(shopcart.email, "advent@change.me")

        # Fetch it back
        shopcart = Shopcart.find(shopcart.id)
        shopcart.email = "XYZZY@plugh.com"
        shopcart.update()

        # Fetch it back again
        shopcart = Shopcart.find(shopcart.id)
        self.assertEqual(shopcart.email, "XYZZY@plugh.com")

    def test_delete_a_shopcart(self):
        """It should Delete a shopcart from the database"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        shopcart = ShopcartFactory()
        shopcart.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(shopcart.id)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)
        shopcart = shopcarts[0]
        shopcart.delete()
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 0)

    def test_find_by_name(self):
        """It should Find an Shopcart by name"""
        shopcart = ShopcartFactory()
        shopcart.create()

        # Fetch it back by name
        same_shopcart = Shopcart.find_by_name(shopcart.name)[0]
        self.assertEqual(same_shopcart.id, shopcart.id)
        self.assertEqual(same_shopcart.name, shopcart.name)

    def test_serialize_a_shopcart(self):
        """It should Serialize a shopcart"""
        shopcart = ShopcartFactory()
        item = ItemFactory()
        shopcart.items.append(item)
        serial_shopcart = shopcart.serialize()
        self.assertEqual(serial_shopcart["id"], shopcart.id)
        self.assertEqual(serial_shopcart["name"], shopcart.name)
        self.assertEqual(serial_shopcart["email"], shopcart.email)
        self.assertEqual(serial_shopcart["phone_number"], shopcart.phone_number)
        self.assertEqual(serial_shopcart["date_joined"], str(shopcart.date_joined))
        self.assertEqual(len(serial_shopcart["items"]), 1)
        items = serial_shopcart["items"]
        self.assertEqual(items[0]["id"], item.id)
        self.assertEqual(items[0]["name"], item.name)
        self.assertEqual(items[0]["quantity"], item.quantity)
        self.assertEqual(items[0]["color"], item.color)
        self.assertEqual(items[0]["size"], item.size)
        self.assertEqual(items[0]["price"], item.price)

    def test_deserialize_a_shopcart(self):
        """It should Deserialize an shopcart"""
        shopcart = ShopcartFactory()
        shopcart.items.append(ItemFactory())
        shopcart.create()
        serial_shopcart = shopcart.serialize()
        new_shopcart = Shopcart()
        new_shopcart.deserialize(serial_shopcart)
        self.assertEqual(new_shopcart.name, shopcart.name)
        self.assertEqual(new_shopcart.email, shopcart.email)
        self.assertEqual(new_shopcart.phone_number, shopcart.phone_number)
        self.assertEqual(new_shopcart.date_joined, shopcart.date_joined)

    def test_deserialize_with_key_error(self):
        """It should not Deserialize a shopcart with a KeyError"""
        shopcart = Shopcart()
        self.assertRaises(DataValidationError, shopcart.deserialize, {})

    def test_deserialize_with_type_error(self):
        """It should not Deserialize a shopcart with a TypeError"""
        shopcart = Shopcart()
        self.assertRaises(DataValidationError, shopcart.deserialize, [])

    def test_deserialize_item_key_error(self):
        """It should not Deserialize a item with a KeyError"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, {})

    def test_deserialize_item_type_error(self):
        """It should not Deserialize a item with a TypeError"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, [])

    ######################################################################
    #  I T E M   T E S T   C A S E S   H E R E
    ######################################################################

    def test_add_a_shopcart(self):

        """It should Create an shopcart and add it to the database"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        shopcart = ShopcartFactory()
        shopcart.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(shopcart.id)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)

    def test_add_shopcart_item(self):

        """It should Create an shopcart with an item and add it to the database"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        shopcart = ShopcartFactory()
        item = ItemFactory(shopcart=shopcart)
        shopcart.items.append(item)
        shopcart.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(shopcart.id)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)

        new_shopcart = Shopcart.find(shopcart.id)
        self.assertEqual(new_shopcart.items[0].name, item.name)

        item2 = ItemFactory(shopcart=shopcart)
        shopcart.items.append(item2)
        shopcart.update()

        new_shopcart = Shopcart.find(shopcart.id)
        self.assertEqual(len(new_shopcart.items), 2)
        self.assertEqual(new_shopcart.items[1].name, item2.name)

    def test_update_shopcart_item(self):
        """It should Update a shopcart's item"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])

        shopcart = ShopcartFactory()
        item = ItemFactory(shopcart=shopcart)
        shopcart.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(shopcart.id)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)

        # Fetch it back
        shopcart = Shopcart.find(shopcart.id)
        old_item = shopcart.items[0]
        print("%r", old_item)
        self.assertEqual(old_item.color, item.color)
        # Change the color
        old_item.color = "XX"
        shopcart.update()

        # Fetch it back again
        shopcart = Shopcart.find(shopcart.id)
        item = shopcart.items[0]
        self.assertEqual(item.color, "XX")

    def test_delete_shopcart_item(self):
        """It should Delete an shopcarts item"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])

        shopcart = ShopcartFactory()
        item = ItemFactory(shopcart=shopcart)
        shopcart.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(shopcart.id)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)

        # Fetch it back
        shopcart = Shopcart.find(shopcart.id)
        item = shopcart.items[0]
        item.delete()
        shopcart.update()

        # Fetch it back again
        shopcart = Shopcart.find(shopcart.id)
        self.assertEqual(len(shopcart.items), 0)
