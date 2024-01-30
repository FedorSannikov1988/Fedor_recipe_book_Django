"""
This module is responsible for generating a unique token.
"""
import jwt
from jwt import DecodeError
from django.conf import settings


class WorkingWithToken:
    """
    Class for working with tokens.

    Attributes:
    - __algoritm: str - the algorithm used for encoding and decoding tokens

    Methods:
    - get_token(self, data: dict) -> str - method to generate a token from data
    - get_data_from_token(self, token: str) -> dict - method to decode a token and retrieve the data

    Example usage:
    token_handler = WorkingWithToken()
    token = token_handler.get_token({'user_id': 123})
    data = token_handler.get_data_from_token(token)
    """

    __algoritm = 'HS256'

    def get_token(self, data: dict) -> str:
        """
        Method to generate a token from data.

        Parameters:
        - data: dict - the data to be encoded in the token

        Returns:
        - str - the generated token

        Description:
        This method encodes the provided data into a token using the SECRET_KEY and the specified algorithm.
        The encoded token is returned as a string.

        Example usage:
        token = get_token({'user_id': 123})
        """
        return jwt.encode(data, settings.SECRET_KEY, algorithm=self.__algoritm)

    def get_data_from_token(self, token: str) -> dict:
        """
        Method to decode a token and retrieve the data.

        Parameters:
        - token: str - the token to be decoded

        Returns:
        - dict - the decoded data from the token

        Description:
        This method decodes the provided token using the SECRET_KEY and the specified algorithm.
        If the decoding is successful, the decoded data is returned as a dictionary.
        If an error occurs during decoding, an empty dictionary is returned.

        Example usage:
        data = get_data_from_token(token)
        """

        decoded_token: dict = {}

        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=self.__algoritm)
            return decoded_token
        except DecodeError:
            return decoded_token