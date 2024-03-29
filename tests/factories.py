# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test Factory to make fake objects for testing
"""
from datetime import date
import factory
from factory.fuzzy import FuzzyChoice, FuzzyDate
from service.models import Shopcart, Item


class ShopcartFactory(factory.Factory):
    """Creates fake Shopcarts"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Persistent class"""

        model = Shopcart

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    email = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    date_joined = FuzzyDate(date(2008, 1, 1))
    # the many side of relationships can be a little wonky in factory boy:
    # https://factoryboy.readthedocs.io/en/latest/recipes.html#simple-many-to-many-relationship

    @factory.post_generation
    def items(
        self, create, extracted, **kwargs
    ):  # pylint: disable=method-hidden, unused-argument
        """Creates the items list"""
        if not create:
            return

        if extracted:
            self.items = extracted


class ItemFactory(factory.Factory):
    """Creates fake Items"""

    # pylint: disable=too-few-public-methods
    class Meta:
        """Persistent class"""

        model = Item

    id = factory.Sequence(lambda n: n)
    shopcart_id = None
    name = FuzzyChoice(choices=["John", "Jane", "Bob"])
    quantity = FuzzyChoice(choices=["1", "2", "3"])
    color = FuzzyChoice(choices=["blue", "red", "green"])
    size = FuzzyChoice(choices=["XS", "S", "L", "XL"])
    price = FuzzyChoice(choices=["10", "20", "30"])
    shopcart = factory.SubFactory(ShopcartFactory)
