"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import datetime
from inventory.views import assignFiscalDay

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class InventoryMethodsTest(TestCase):
    def test_twoam_delivery_or_collection(self):
        """
        2 am on 5.7 should generate a fiscal day of 5.6
        """
        dt = datetime.datetime(2013, 5, 7, 03, 00)
        fiscal_day = datetime.datetime(2013, 5, 6)
        two_am_delivery_or_collection = assignFiscalDay(dt)

        self.assertEqual(two_am_delivery_or_collection, fiscal_day)

"""
    def test_record_token_collection(TestCase):
        dt = datetime.datetime(2013, 5, 7, 03, 00)
        fiscal_day = datetime.datetime(2013, 5, 6)
        self.assertEqual(two_am_delivery_or_collection, fiscal_day)
"""
