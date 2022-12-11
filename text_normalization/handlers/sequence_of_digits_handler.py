import phonenumbers

from . import BaseHandler, spell_out_number


class SequenceOfDigitsHandler(BaseHandler):
    """
    normalize phone numbers to their full text equivalent
    """

    def _handle(self, ctx: str) -> str:
        """handle contexts containing phone numbers

        Args:
            ctx (str): textual context

        Returns:
            str: normalization output
        """
        data = ctx
        words = []
        for char in data:
            if char.isdigit():
                words.append(spell_out_number(char))

        return self._format(words)

    @staticmethod
    def _format(data: list) -> str:
        """construct final representation of result

        Args:
            data (str): textual phone number

        Returns:
            str: formatted result
        """
        return "{}".format(" ".join(data))
