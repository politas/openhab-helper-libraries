""" Test helper library  """

import unittest
import time
from core.items import add_item, remove_item
from core.utils import get_item_state
from core.log import logging, LOG_PREFIX
from core.jsr223.scope import events, ON, OFF, StringType, DateTimeType, DecimalType
from core.jsr223.scope import PercentType, QuantityType, UnitType, HSBType, PointType, OnOffType
from core.jsr223 import scope
from core.testing import run_test
from java.time import ZonedDateTime
from datetime import datetime

log = logging.getLogger("{}.OHL-test-core.utils".format(LOG_PREFIX))

test_item = "DogeTest" #Change if you have an actual item with this name

log.info("Starting test script")


class CoreUtilsTestCase(unittest.TestCase):
	def get_item_state_returns_equality(self, test_item, test_type, test_value, expected, return_type=None, unit=None):
		#remove_item(test_item)
		item = add_item(test_item, item_type=test_type)
		events.postUpdate(item, test_value)
		time.sleep(0.5)
		result = get_item_state(test_item, return_type=return_type, unit=unit)
		remove_item(item)
		self.assertEqual(result, expected,
			msg="Function get_item_state on created '{}' item should return '{}' but returned '{}'".format(
				test_type,
				expected,
				result))

	def get_item_state_returns_correct_type(self, test_item, test_type, test_value, expected_type, return_type=None):
		#remove_item(test_item)
		item = add_item(test_item, item_type=test_type)
		events.postUpdate(item, test_value)
		time.sleep(0.5)
		result = get_item_state(test_item, return_type=return_type)
		remove_item(item)
		self.assertIsInstance(result, expected_type,
			msg="Function get_item_state on '{}' item should return type '{}' but returned type '{}'".format(
				test_type, 
				expected_type.__name__, 
				type(result).__name__))

	def test_get_item_state_returns_none_for_non_existing_item_with_no_default(self):
		#remove_item("DogeDoesNotExist")
		result = get_item_state("DogeDoesNotExist")
		self.assertIsNone(result, 
			msg="Function get_item_state on non existent item with no default should be None but returned '{}'".format(result))
	
	def test_get_item_state_returns_default_for_non_existing_item_with_default(self):
		#remove_item("DogeDoesNotExist")
		expected = "5 Dogecoins"
		result = get_item_state("DogeDoesNotExist", default=expected)
		self.assertEqual(result, expected,
			msg="Function get_item_state on non existent item with default should be '{}' but returned '{}'".format(expected, result))

	def test_get_item_state_returns_expected_string_for_string_item(self):
		test_value = StringType("5 Dogecoins")
		self.get_item_state_returns_equality("DogeString", "String", test_value, test_value)

	def test_get_item_state_returns_expected_datetime_for_datetime_item(self):
		test_value = DateTimeType("1991-12-21T12:21:19")
		self.get_item_state_returns_equality("DogeDate", "DateTime", test_value, test_value)

	def test_get_item_state_returns_expected_number_for_number_item(self):
		test_value = DecimalType(55.5)
		self.get_item_state_returns_equality("DogeNumber", "Number", test_value, test_value)

	def test_get_item_state_returns_expected_percentage_for_dimmer_item(self):
		test_value = PercentType(55)
		self.get_item_state_returns_equality("DogeDimmer", "Dimmer", test_value, test_value)
	
	def test_get_item_state_returns_expected_color_for_color_item(self):
		test_value = HSBType(DecimalType(55), PercentType(55), PercentType(55))
		self.get_item_state_returns_equality("DogeColor", "Color", test_value, test_value)

	def test_get_item_state_returns_farenheit_for_number_item_with_unit(self):
		test_value = QuantityType(u"55.0 °C")
		expected = QuantityType(u"131.0 °F")
		test_unit = u"°F"
		self.get_item_state_returns_equality("DogeTemp", "Number", test_value, expected, unit=test_unit)

	def test_get_item_state_returns_expected_string_for_number_item_with_return_type(self):
		test_value = DecimalType(55.5)
		expected = "55.5"
		test_return = str
		self.get_item_state_returns_equality("DogeNumber", "Number", test_value, expected, return_type=test_return)

	def test_get_item_state_returns_expected_int_for_number_item_with_return_type(self):
		test_value = DecimalType(55.5)
		expected = 55
		test_return = int
		self.get_item_state_returns_equality("DogeNumber", "Number", test_value, expected, return_type=test_return)
		
	def test_get_item_state_returns_StringType_for_string_item(self):
		test_value = StringType("5 Dogecoins")
		self.get_item_state_returns_correct_type("DogeString", "String", test_value, StringType)
	
	def test_get_item_state_returns_DateTimeType_for_date_item(self):
		test_value = DateTimeType("1991-12-21T12:21:19")
		self.get_item_state_returns_correct_type("DogeDate", "DateTime", test_value, DateTimeType)
	
	def test_get_item_state_returns_DecimalType_for_number_item(self):
		test_value = DecimalType(55.5)
		self.get_item_state_returns_correct_type("DogeNumber", "Number", test_value, DecimalType)

	def test_get_item_state_returns_PercentType_for_dimmer_item(self):
		test_value = PercentType(55)
		self.get_item_state_returns_correct_type("DogeDimmer", "Dimmer", test_value, PercentType)

	def test_get_item_state_returns_ColorType_for_color_item(self):
		test_value = HSBType(DecimalType(55), PercentType(55), PercentType(55))
		self.get_item_state_returns_correct_type("DogeColor", "Color", test_value, HSBType)

	def test_get_item_state_returns_datetime_for_date_item_with_return_type(self):
		test_value = DateTimeType("1991-12-21T12:21:19")
		self.get_item_state_returns_correct_type("DogeDate", "DateTime", test_value, datetime, return_type=datetime)

	def test_get_item_state_returns_ZonedDateTime_for_date_item_with_return_type(self):
		test_value = DateTimeType("1991-12-21T12:21:19")
		self.get_item_state_returns_correct_type("DogeDate", "DateTime", test_value, ZonedDateTime, return_type=ZonedDateTime)

	
run_test(CoreUtilsTestCase, logger=log)


