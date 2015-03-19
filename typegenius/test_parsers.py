import unittest
from datetime import datetime
from typegenius import parsers


class TestParsers(unittest.TestCase):
    def test_is_float_valid_instance(self):
        val = 1.2
        self.assertTrue(parsers.is_float(val))

    def test_is_float_valid_string(self):
        val = '1.2'
        self.assertTrue(parsers.is_float(val))

    def test_is_float_invalid(self):
        val = 'abc'
        self.assertFalse(parsers.is_float(val))

    def test_is_int_valid_instance(self):
        val = 1
        self.assertTrue(parsers.is_int(val))

    def test_is_int_valid_string(self):
        val = '1'
        self.assertTrue(parsers.is_int(val))

    def test_is_int_invalid(self):
        val = 'abc'
        self.assertFalse(parsers.is_int(val))

    def test_is_bool_valid_instance(self):
        val = True
        self.assertTrue(parsers.is_bool(val))

    def test_is_bool_valid_string_true(self):
        val = 'TRUE'
        self.assertTrue(parsers.is_bool(val))

    def test_is_bool_valid_string_false(self):
        val = 'false'
        self.assertTrue(parsers.is_bool(val))

    def test_is_bool_invalid(self):
        val = 'abc'
        self.assertFalse(parsers.is_bool(val))

    def test_is_date_valid_instance(self):
        val = datetime.now()
        self.assertTrue(parsers.is_date(val))

    def test_is_date_rfc_3339_allows_t_replacement(self):
        val = '2011-10-05 22:26:12-04:00'
        self.assertTrue(parsers.is_date_rfc_3339(val))

    def test_is_date_rfc_3339_allows_negative_zero(self):
        val = '2011-10-05 22:26:12-00:00'
        self.assertTrue(parsers.is_date_rfc_3339(val))

    def test_is_date_rfc_3339_requires_full_date_time(self):
        val = '2011-10-05'
        self.assertFalse(parsers.is_date_rfc_3339(val))

    def test_is_date_rfc_3339_requires_period_fractions(self):
        val = '2011-10-05T22:26:12,123-04:00'
        self.assertFalse(parsers.is_date_rfc_3339(val))

    def test_is_date_iso_8601_allows_omitting_time(self):
        val = '2011-10-05'
        self.assertTrue(parsers.is_date_iso_8601(val))

    def test_is_date_iso_8601_requires_at_least_date(self):
        val = '12'
        self.assertFalse(parsers.is_date_iso_8601(val))

    def test_is_date_iso_8601_allows_period_comma_fractions(self):
        val = '2011-10-05T22:26:12,123+04:00'
        self.assertTrue(parsers.is_date_iso_8601(val))

    def test_is_date_iso_8601_disallows_negative_zero(self):
        val = '2011-10-05T22:26:12-00:00'
        self.assertFalse(parsers.is_date_iso_8601(val))

    def test_get_float(self):
        val = 1.2
        result = parsers.get(str(val))
        self.assertEqual(val, result)

    def test_get_int(self):
        val = 1
        result = parsers.get(str(val))
        self.assertEqual(val, result)

    def test_get_bool(self):
        val = True
        result = parsers.get(str(val))
        self.assertEqual(val, result)

    def test_get_date_by_year_month_day(self):
        val = datetime(2010, 1, 1)
        result = parsers.get(val.strftime('%Y-%m-%d'))
        self.assertEqual(val, result)

    def test_get_date_by_year_month_day_hour(self):
        val = datetime(2010, 1, 1, 1)
        result = parsers.get(val.strftime('%Y-%m-%dT%H'))
        self.assertEqual(val, result)

    def test_get_date_by_year_month_day_hour_minute(self):
        val = datetime(2010, 1, 1, 1, 1)
        result = parsers.get(val.strftime('%Y-%m-%dT%H:%M'))
        self.assertEqual(val, result)

    def test_get_date_with_z(self):
        val = datetime.strptime('2015-03-16T13:29:14.50+0000', '%Y-%m-%dT%H:%M:%S.%f%z')
        result = parsers.get('2015-03-16T13:29:14.50Z')
        self.assertEqual(val, result)

    def test_get_date_with_timezone(self):
        val = datetime.strptime('2015-03-16T13:29:14.550+0200', '%Y-%m-%dT%H:%M:%S.%f%z')
        result = parsers.get('2015-03-16T13:29:14.550+0200')
        self.assertEqual(val, result)