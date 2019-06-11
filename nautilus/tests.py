import datetime
from django.test import TestCase

import nautilus.models as m
import nautilus.queries as q
import nautilus.utils as u

class UtilsTestCase(TestCase):
    def setUp(self):
        self.empty_string = ''
        self.null_string = None
        self.yyyy_only = '2019'
        self.yyyymm_month_one_digit = '20198'
        self.yyyymmdd = '20190801'
        self.raw_date = datetime.datetime.now()
        self.not_numerical_string = 'ABCDEFG'
        self.valid_string = '201901'

    def test_yyyymmToMonthName(self):
        # bad formatted inputs should not raise an exception and return input
        self.assertTrue(self.empty_string == u.yyyymmToMonthName(self.empty_string))
        self.assertTrue(self.null_string == u.yyyymmToMonthName(self.null_string))
        self.assertTrue(self.yyyy_only == u.yyyymmToMonthName(self.yyyy_only))
        self.assertTrue(self.yyyymm_month_one_digit == u.yyyymmToMonthName(self.yyyymm_month_one_digit))
        self.assertTrue(self.yyyymmdd == u.yyyymmToMonthName(self.yyyymmdd))
        self.assertTrue(self.raw_date == u.yyyymmToMonthName(self.raw_date))
        self.assertTrue(self.not_numerical_string == u.yyyymmToMonthName(self.not_numerical_string))
        self.assertTrue('2019-Jan' == u.yyyymmToMonthName(self.valid_string))


    def test_yyyymm_add_months(self):
        self.assertTrue(self.empty_string == u.yyyymm_add_months(self.empty_string, 2))
        self.assertTrue(self.null_string == u.yyyymm_add_months(self.null_string, 5))
        self.assertTrue(self.yyyy_only == u.yyyymm_add_months(self.yyyy_only, -1))
        self.assertTrue(self.yyyymm_month_one_digit == u.yyyymm_add_months(self.yyyymm_month_one_digit, -3))
        self.assertTrue(self.yyyymmdd == u.yyyymm_add_months(self.yyyymmdd, 4))
        self.assertTrue(self.raw_date == u.yyyymm_add_months(self.raw_date, -1))
        self.assertTrue(self.not_numerical_string == u.yyyymm_add_months(self.not_numerical_string, 5))
        self.assertTrue(self.valid_string == u.yyyymm_add_months(self.valid_string, self.not_numerical_string))
        self.assertTrue('201810' == u.yyyymm_add_months(self.valid_string, -3))
        self.assertTrue('201905' == u.yyyymm_add_months(self.valid_string, 4))

