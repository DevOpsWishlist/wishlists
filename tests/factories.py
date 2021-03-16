"""
Test Factory to make fake objects for testing
"""
import factory
from datetime import datetime
from factory.fuzzy import FuzzyChoice
from service.models import WishList, Item

class ItemFactory(factory.Factory):
    """ Creates fake Addresses """

    class Meta:
        model = Item

    id = factory.Sequence(lambda n: n)
#    account_id = ???
    name = FuzzyChoice(choices=["item1", "item2", "item3"])
    price = factory.Faker(88)


class WishListFactory(factory.Factory):
    """ Creates fake Accounts """

    class Meta:
        model = WishList

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    category = factory.Faker("category1")

