import re

from phonenumbers import PhoneNumberMatcher
from text_normalization.constants import cardinal, indic2latin

from . import BaseStep


class NormalizePhoneNumbers(BaseStep):
    """
    Finds phone number in the given txt and replaces it with its
    equivalent audiable words. Only numbers with a leading plus
    are considered.
    """

    def process(self, request: dict, config: dict):

        for sentence in request["sentences"]:

            if not self.hasdigits(sentence.text):
                continue

        return self.process_next(request, config)

    @staticmethod
    def convert_phone(phone_number):
        """
        uses a map from the constants file to normalize numbers
        """

        converted_chars = []
        for char in phone_number:

            if char in cardinal:
                converted_chars.append(cardinal[char])

            elif char in indic2latin:
                converted_chars.append(cardinal[indic2latin[char]])

            else:
                pass

        return " ".join(converted_chars)

    @staticmethod
    def hasdigits(text):
        """
        Checks if the provided text has any digits
        """

        catcher = re.compile(r"[0-9]")
        return catcher.search(text)
