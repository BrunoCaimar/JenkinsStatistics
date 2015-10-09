"""
Date Range related functions
"""
import datetime


def get_months_array(initial_month_year,
                     number_of_months_to_get):
    """
    Get months array based on initial month and number of months to get
    :param initial_month_year: Initial month e.g. (1,2015)
    :param number_of_months_to_get: Number of months to get eg: 2
    :return: Array with month/year data e.g [(12,2014), (1,2015)]
    """
    months_array = [initial_month_year]

    for item in range(1, number_of_months_to_get):
        month = initial_month_year[0]
        year = initial_month_year[1]
        month += item

        if month > 12:
            month -= 12
            year += 1

        months_array.append((month, year))
    return months_array


def get_starting_month(number_of_months_to_get,
                       include_actual_month=True,
                       actual_date=datetime.datetime.now()):
    """
    Get starting month based on parameters
    :param number_of_months_to_get: Numbers of months to get - e.g: 2
    :param include_actual_month: Include actual month? e.g.: True
    :param actual_date: Actual Date e.g: now()
    :return: :raise Exception: if number_of_months_to_get less than 1
    Initial month\year e.g: (12,2014)
    """
    if number_of_months_to_get <= 0:
        raise Exception("Number of month's to get should be greater than 0")

    initial_year = actual_date.year

    if actual_date.month > number_of_months_to_get:
        initial_month = actual_date.month - number_of_months_to_get
    else:
        initial_month = actual_date.month - number_of_months_to_get

        if initial_month <= 0:
            initial_month += 12
            initial_year -= 1

    if include_actual_month:
        initial_month += 1
        if initial_month > 12:
            initial_month = 1
            initial_year += 1

    return initial_month, initial_year
