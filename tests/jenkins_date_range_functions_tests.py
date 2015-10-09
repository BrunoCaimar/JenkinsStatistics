import datetime
from unittest import TestCase
from JenkinsStatistics.jenkins_date_range_functions import get_months_array, get_starting_month


class DateRelatedFunctionsTests(TestCase):

    def test_get_months_array_for_one_month_should_return_one_month_only(self):
        fake_actual_date = datetime.datetime(2015, 10, 1)
        number_of_months_to_get = 1
        starting_month = get_starting_month(number_of_months_to_get,
                                            actual_date=fake_actual_date)
        print 'starting_month', starting_month
        months_array = get_months_array(starting_month,
                                        number_of_months_to_get)
        self.assertEqual(1, len(months_array))
        self.assertEqual((10, 2015), months_array[0])

    def test_get_months_array_for_two_months_should_return_two_months(self):
        fake_actual_date = datetime.datetime(2015, 1, 1)
        number_of_months_to_get = 2
        starting_month = get_starting_month(number_of_months_to_get,
                                            actual_date=fake_actual_date)
        print 'starting_month', starting_month
        months_array = get_months_array(starting_month,
                                        number_of_months_to_get)
        self.assertEqual(2, len(months_array))
        self.assertEqual((12, 2014), months_array[0])
        self.assertEqual((1, 2015), months_array[1])

    def test_get_months_array_for_12_months_should_return_12_months_different_years(self):
        fake_actual_date = datetime.datetime(2015, 10, 1)
        number_of_months_to_get = 12
        starting_month = get_starting_month(number_of_months_to_get,
                                            actual_date=fake_actual_date)
        print 'starting_month', starting_month
        months_array = get_months_array(starting_month,
                                        number_of_months_to_get)

        print 'months_array', months_array

        self.assertEqual(12, len(months_array))
        self.assertEqual((11, 2014), months_array[0])
        self.assertEqual((12, 2014), months_array[1])
        self.assertEqual((1, 2015), months_array[2])
        self.assertEqual((2, 2015), months_array[3])
        self.assertEqual((3, 2015), months_array[4])
        self.assertEqual((4, 2015), months_array[5])
        self.assertEqual((5, 2015), months_array[6])
        self.assertEqual((6, 2015), months_array[7])
        self.assertEqual((7, 2015), months_array[8])
        self.assertEqual((8, 2015), months_array[9])
        self.assertEqual((9, 2015), months_array[10])
        self.assertEqual((10, 2015), months_array[11])

    def test_get_starting_month_for_invalid_parameters_should_raise_exception(
            self):
        fake_actual_date = datetime.datetime(2015, 1, 1)

        with self.assertRaisesRegexp(Exception, "Number of month's to get should be greater than 0"):
            get_starting_month(0, actual_date=fake_actual_date)

    def test_get_starting_month_for_actual_month_10_and_number_of_months_1_and_include_actual_month_should_return_10(
            self):
        fake_actual_date = datetime.datetime(2015, 10, 1)

        starting_month = get_starting_month(1,
                                            actual_date=fake_actual_date)
        print starting_month
        self.assertEqual((10, 2015), starting_month)

    def test_get_starting_month_for_actual_month_1_and_number_of_months_1_and_not_include_actual_month_should_return_1(
            self):
        fake_actual_date = datetime.datetime(2015, 1, 1)

        starting_month = get_starting_month(1,
                                            actual_date=fake_actual_date)
        self.assertEqual((1, 2015), starting_month)

    def test_get_starting_month_for_actual_month_1_and_number_of_months_1_and_not_include_actual_month_should_return_12(
            self):
        fake_actual_date = datetime.datetime(2015, 1, 1)

        starting_month = get_starting_month(1,
                                            include_actual_month=False,
                                            actual_date=fake_actual_date)
        self.assertEqual((12, 2014), starting_month)

    def test_get_starting_month_for_month_10_and_number_of_months_10_and_not_include_actual_month_should_return_12(
            self):
        fake_actual_date = datetime.datetime(2015, 10, 1)
        starting_month = get_starting_month(10,
                                            include_actual_month=False,
                                            actual_date=fake_actual_date)
        self.assertEqual((12, 2014), starting_month)

    def test_get_starting_month_for_actual_month_10_and_number_of_months_10_should_return_1(self):
        fake_actual_date = datetime.datetime(2015, 10, 1)
        starting_month = get_starting_month(10,
                                            actual_date=fake_actual_date)
        self.assertEqual((1, 2015), starting_month)

    def test_get_starting_month_for_actual_month_10_and_number_of_months_12_should_return_11(self):
        fake_actual_date = datetime.datetime(2015, 10, 1)
        starting_month = get_starting_month(12,
                                            actual_date=fake_actual_date)
        self.assertEqual((11, 2014), starting_month)

    def test_get_starting_month_for_actual_month_10_and_number_of_months_6_should_return_4(self):
        fake_actual_date = datetime.datetime(2015, 10, 1)
        starting_month = get_starting_month(6,
                                            actual_date=fake_actual_date)
        self.assertEqual((5, 2015), starting_month)

    def test_get_starting_month_for_actual_month_10_and_number_of_months_6_and_not_include_actual_month_should_return_3(
            self):
        fake_actual_date = datetime.datetime(2015, 10, 1)
        starting_month = get_starting_month(6,
                                            include_actual_month=False,
                                            actual_date=fake_actual_date)
        self.assertEqual((4, 2015), starting_month)
