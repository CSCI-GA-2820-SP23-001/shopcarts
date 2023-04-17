"""
Shopcart API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""

import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from tests.factories import ShopcartFactory, ItemFactory
from service.common import status  # HTTP Status Codes
from service.models import db, Shopcart, init_db
from service.routes import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

BASE_URL = "/shopcarts"

######################################################################
#  T E S T   C A S E S
######################################################################


class TestShopcartService(TestCase):
    """Shopcart Service Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    def tearDownClass(cls):
        """Runs once before test suite"""

    def setUp(self):
        """Runs before each test"""
        db.session.query(Shopcart).delete()  # clean up the last tests
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """Runs once after each test case"""
        db.session.remove()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_shopcarts(self, count):
        """Factory method to create shopcarts in bulk"""
        shopcarts = []
        for _ in range(count):
            shopcart = ShopcartFactory()
            resp = self.client.post(BASE_URL, json=shopcart.serialize())
            self.assertEqual(
                resp.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Shopcart",
            )
            new_shopcart = resp.get_json()
            shopcart.id = new_shopcart["id"]
            shopcarts.append(shopcart)
        return shopcarts

    ######################################################################
    #  S H O P C A R T   T E S T   C A S E S   H E R E
    ######################################################################

    def test_create_shopcart(self):
        """It should Create a new Shopcart"""
        shopcart = ShopcartFactory()
        resp = self.client.post(
            BASE_URL, json=shopcart.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_shopcart = resp.get_json()
        self.assertEqual(new_shopcart["name"], shopcart.name, "Names does not match")
        self.assertEqual(new_shopcart["email"], shopcart.email, "Email does not match")
        self.assertEqual(
            new_shopcart["phone_number"], shopcart.phone_number, "Phone does not match"
        )
        self.assertEqual(
            new_shopcart["date_joined"],
            str(shopcart.date_joined),
            "Date Joined does not match",
        )

    def test_get_shopcart_list(self):
        """It should Get a list of Shopcarts"""
        self._create_shopcarts(5)
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_get_shopcart_by_name(self):
        """It should Get a Shopcart by Name"""
        shopcarts = self._create_shopcarts(3)
        resp = self.client.get(BASE_URL, query_string=f"name={shopcarts[1].name}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data[0]["name"], shopcarts[1].name)

    def test_get_shopcart_by_email(self):
        """It should Get a Shopcart by Email"""
        shopcarts = self._create_shopcarts(3)
        resp = self.client.get(BASE_URL, query_string=f"email={shopcarts[1].email}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data[1]["email"], shopcarts[1].email)
    
    def test_get_shopcart(self):
        """It should Read a single Shopcart"""
        # get the id of an shopcart
        shopcart = self._create_shopcarts(1)[0]
        resp = self.client.get(
            f"{BASE_URL}/{shopcart.id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], shopcart.name)

    def test_get_shopcart_not_found(self):
        """It should not Read an Shopcart that is not found"""
        resp = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_shopcart(self):
        """It should Update an existing Shopcart"""
        # create an Shopcart to update
        test_shopcart = ShopcartFactory()
        resp = self.client.post(BASE_URL, json=test_shopcart.serialize())
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the shopcart
        new_shopcart = resp.get_json()
        new_shopcart["name"] = "Happy-Happy Joy-Joy"
        new_shopcart_id = new_shopcart["id"]
        resp = self.client.put(f"{BASE_URL}/{new_shopcart_id}", json=new_shopcart)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_shopcart = resp.get_json()
        self.assertEqual(updated_shopcart["name"], "Happy-Happy Joy-Joy")

    def test_delete_shopcart(self):
        """It should Delete an Shopcart"""
        # get the id of an shopcart
        shopcart = self._create_shopcarts(1)[0]
        resp = self.client.delete(f"{BASE_URL}/{shopcart.id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    ######################################################################
    #   I T E M   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the Home Page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_health_endpoint(self):
        """It should call the health endpoint and return OK"""
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["status"], "OK")

    def test_add_item(self):
        """It should Add an item to an shopcart"""
        shopcart = self._create_shopcarts(1)[0]
        item = ItemFactory()
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["shopcart_id"], shopcart.id)
        self.assertEqual(data["name"], item.name)
        self.assertEqual(data["quantity"], item.quantity)
        self.assertEqual(data["color"], item.color)
        self.assertEqual(data["size"], item.size)
        self.assertEqual(data["price"], item.price)

    def test_get_item(self):
        """It should Get an item from an shopcart"""
        # create a known item
        shopcart = self._create_shopcarts(1)[0]
        item = ItemFactory()
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        item_id = data["id"]

        # retrieve it back
        resp = self.client.get(
            f"{BASE_URL}/{shopcart.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["shopcart_id"], shopcart.id)
        self.assertEqual(data["name"], item.name)
        self.assertEqual(data["quantity"], item.quantity)
        self.assertEqual(data["color"], item.color)
        self.assertEqual(data["size"], item.size)
        self.assertEqual(data["price"], item.price)

    def test_get_item_list(self):
        """It should Get a list of Items"""
        # add two items to shopcart
        shopcart = self._create_shopcarts(1)[0]
        item_list = ItemFactory.create_batch(2)

        # Create item 1
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/items", json=item_list[0].serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Create item 2
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/items", json=item_list[1].serialize()
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # get the list back and make sure there are 2
        resp = self.client.get(f"{BASE_URL}/{shopcart.id}/items")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        self.assertEqual(len(data), 2)

    def test_update_item(self):
        """It should Update an item in a shopcart"""
        # create a known item
        shopcart = self._create_shopcarts(1)[0]
        item = ItemFactory()
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        item_id = data["id"]
        data["name"] = "XXXX"

        # send the update back
        resp = self.client.put(
            f"{BASE_URL}/{shopcart.id}/items/{item_id}",
            json=data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # retrieve it back
        resp = self.client.get(
            f"{BASE_URL}/{shopcart.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        logging.debug(data)
        self.assertEqual(data["id"], item_id)
        self.assertEqual(data["shopcart_id"], shopcart.id)
        self.assertEqual(data["name"], "XXXX")

    def test_delete_item(self):
        """It should Delete an Item"""
        shopcart = self._create_shopcarts(1)[0]
        item = ItemFactory()
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)
        item_id = data["id"]

        # send delete request
        resp = self.client.delete(
            f"{BASE_URL}/{shopcart.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        # retrieve it back and make sure item is not there
        resp = self.client.get(
            f"{BASE_URL}/{shopcart.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    ######################################################################
    #  T E S T   A C T I O N S
    ######################################################################

    def test_increment_an_item(self):
        """It should increase the quantity of an item"""
        # create a known item
        shopcart = self._create_shopcarts(1)[0]
        item = ItemFactory()
        resp = self.client.post(
            f"{BASE_URL}/{shopcart.id}/items",
            json=item.serialize(),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        item_id = data["id"]

        old_quantity = int(item.quantity)
        new_quantity = str(old_quantity + 1)

        resp = self.client.put(
            f"{BASE_URL}/{shopcart.id}/items/{item_id}/increment",
            json=data,
            content_type="application/json",
        )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        logging.debug("Response data: %s", data)
        self.assertEqual(data["quantity"], new_quantity)

    def test_decrement_an_item(self):
        """It should decrease the quantity of an item"""

        old_quantity = 1

        while old_quantity < 2:
            # create a known item
            shopcart = self._create_shopcarts(1)[0]
            item = ItemFactory()
            resp = self.client.post(
                f"{BASE_URL}/{shopcart.id}/items",
                json=item.serialize(),
                content_type="application/json",
            )

            old_quantity = int(item.quantity)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        item_id = data["id"]

        new_quantity = str(old_quantity - 1)

        resp = self.client.put(
            f"{BASE_URL}/{shopcart.id}/items/{item_id}/decrement",
            json=data,
            content_type="application/json",
        )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()

        logging.debug("Response data: %s", data)
        self.assertEqual(data["quantity"], new_quantity)

    def test_decrement_single_item(self):
        """If decrementing the quantity of a single item, the item should be deleted"""

        old_quantity = 2

        while old_quantity != 1:
            # create a known item
            shopcart = self._create_shopcarts(1)[0]
            item = ItemFactory()
            resp = self.client.post(
                f"{BASE_URL}/{shopcart.id}/items",
                json=item.serialize(),
                content_type="application/json",
            )

            old_quantity = int(item.quantity)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        data = resp.get_json()
        logging.debug(data)
        item_id = data["id"]

        resp = self.client.put(
            f"{BASE_URL}/{shopcart.id}/items/{item_id}/decrement",
            json=data,
            content_type="application/json",
        )

        # retrieve it back and make sure item is not there
        resp = self.client.get(
            f"{BASE_URL}/{shopcart.id}/items/{item_id}",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    ######################################################################
    #   O T H E R   T E S T   C A S E S
    ######################################################################

    def test_bad_request(self):
        """It should not Create when sending the wrong data"""
        resp = self.client.post(BASE_URL, json={"name": "not enough data"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsupported_media_type(self):
        """It should not Create when sending wrong media type"""
        shopcart = ShopcartFactory()
        resp = self.client.post(
            BASE_URL, json=shopcart.serialize(), content_type="test/html"
        )
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_method_not_allowed(self):
        """It should not allow an illegal method call"""
        resp = self.client.put(BASE_URL, json={"not": "today"})
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
