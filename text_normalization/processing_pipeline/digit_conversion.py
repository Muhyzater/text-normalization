import re

from . import BaseStep


class DigitConversion(BaseStep):
    """
    This step unifies all digits to english numbers
    """

    def process(self, request: dict, config: dict):
        request["text"] = self.convert_ar_numbers(request["text"])
        return self.process_next(request, config)

    @staticmethod
    def convert_ar_numbers(text):
        """
        This function convert Arabic numbers to English numbers.

        Keyword arguments:
        text -- It should be string
        Returns: English numbers
        """
        mapping = {
            "٠": "0",
            "١": "1",
            "٢": "2",
            "٣": "3",
            "٤": "4",
            "٥": "5",
            "٦": "6",
            "٧": "7",
            "٨": "8",
            "٩": "9",
        }
        pattern = "|".join(map(re.escape, mapping.keys()))
        return re.sub(pattern, lambda m: mapping[m.group()], str(text))
