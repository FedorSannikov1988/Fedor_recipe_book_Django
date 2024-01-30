"""
This module is responsible for working with the date and time inside the application.
"""
from datetime import datetime, \
                     timedelta
from django.conf import settings


class WorkingWithTimeInsideApp:
    """
    Class for working with time inside the app.

    Attributes:
    - __data_format: str - the format for date strings
    - __number_days_per_year: int - the number of days in a year
    - __data_and_time_format: str - the format for date and time strings

    Methods:
    - checking_user_age(self, date_birth) -> bool - method to check if a user's age is within a certain range
    - get_data_and_time(self) -> str - method to get the current date and time
    - checking_date_and_time_registration_user(self, date_and_time_registration_user: str) -> bool - method to check if the date and time of user registration is within a certain range
    - checking_time_password_recovery_request(self, time_receipt_request: str) -> bool - method to check if the time of a password recovery request is within a certain range

    Example usage:
    time_app = WorkingWithTimeInsideApp()
    is_age_valid = time_app.checking_user_age('1990-01-01')
    current_datetime = time_app.get_data_and_time()
    is_registration_valid = time_app.checking_date_and_time_registration_user('01.01.2022 10:00:00')
    is_recovery_valid = time_app.checking_time_password_recovery_request('01.01.2022 12:00:00')
    """

    __data_format: str = "%Y-%m-%d"
    __number_days_per_year: int = 365
    __data_and_time_format: str = "%d.%m.%Y %H:%M:%S"

    def checking_user_age(self, date_birth) -> bool:
        """
         Method to check if a user's age is within a certain range.

        :param date_birth: datetime.data -> the date of birth in the format 'YYYY-MM-DD'.
        :return: bool -> True if the user's age is within the range, False otherwise.

        Description:
        This method checks if the user's age, calculated based on the provided date of birth,
        is within the range defined by the constants LOWER_AGE_YEARS and UPPER_AGE_YEARS.
        The age is calculated by comparing the current date with the date of birth.
        """
        date_birt_str: str = str(date_birth)

        for_lower_bound: timedelta = \
            timedelta(days=
                      self.__number_days_per_year * settings.LOWER_AGE_YEARS)

        for_upper_bound: timedelta = \
            timedelta(days=
                      self.__number_days_per_year * settings.UPPER_AGE_YEARS)

        date_now: datetime = datetime.now()

        lower_bound = \
            date_now - for_lower_bound

        upper_bound = \
            date_now - for_upper_bound

        conversion_date = \
            datetime.strptime(date_birt_str, self.__data_format)

        return upper_bound <= conversion_date <= lower_bound

    def get_data_and_time(self) -> str:
        """
        Method to get the current date and time.

        Parameters:
        - None

        :return:str -> the current date and time in the format 'DD.MM.YYYY HH:MM:SS'

        Description:
        This method returns the current date and time as a formatted string.
        The format is defined by the __data_and_time_format attribute.

        Example usage:
        current_datetime = get_data_and_time()
        """
        return datetime.now().strftime(self.__data_and_time_format)

    def checking_date_and_time_registration_user(self,
                                                 date_and_time_registration_user: str) -> bool:
        """
         Method to check if the date and time of user registration is within a certain range.


        :param date_and_time_registration_user: str -> date and time of user registration in the format 'DD.MM.YYYY HH:MM:SS'

        :return: bool -> True if the date and time of user registration is within the range, False otherwise

        Description:
        This method checks if the date and time of user registration, provided as a string,
        is within the range defined by the constant TIME_TO_ACTIVATE_ACCOUNT_HOURS.
        The range is calculated by adding the specified number of hours to the date and time of registration
        and comparing it with the current date and time.

        Example usage:
        is_registration_valid = checking_date_and_time_registration_user('01.01.2022 10:00:00')
        """
        conversion_date = \
            datetime.strptime(date_and_time_registration_user,
                              self.__data_and_time_format)

        return conversion_date + timedelta(hours=settings.TIME_TO_ACTIVATE_ACCOUNT_HOURS) >= datetime.now()

    def checking_time_password_recovery_request(self,
                                                time_receipt_request: str) -> bool:
        """
        Method to check if the time of a password recovery request is within a certain range.


        :param time_receipt_request: str -> the time of the password recovery request inthe format 'DD.MM.YYYY HH:MM:SS'
        :return: bool -> True if the time of the password recovery request is within the range, False otherwise

        Description:
        This method checks if the time of the password recovery request, provided as a string,
        is within the range defined by the constant DURATION_PASSWORD_RECOVERY_LINK_MINUTES.
        The range is calculated by adding the specified number of minutes to the time of the request
        and comparing it with the current date and time.

        Example usage:
        is_recovery_valid = checking_time_password_recovery_request('01.01.2022 12:00:00')
        """

        conversion_date = \
            datetime.strptime(time_receipt_request,
                              self.__data_and_time_format)

        return conversion_date + timedelta(minutes=settings.DURATION_PASSWORD_RECOVERY_LINK_MINUTES) >= datetime.now()

