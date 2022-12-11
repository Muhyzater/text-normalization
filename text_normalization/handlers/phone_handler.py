import phonenumbers

from . import BaseHandler, spell_out_number, NotEmpty, isPhone


class PhoneHandler(BaseHandler):
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
        endOfText = ""

        if not data[-1].isdigit():
            endOfText += data[-1]
            data = data[:-1]

        if data.startswith("+"):
            data = "00" + data[1:]

        return self._restore_seprartor(self._format(spell_out_number(data)), endOfText)

    @staticmethod
    def _format(data: str) -> str:
        """construct final representation of result

        Args:
            data (str): textual phone number

        Returns:
            str: formatted result
        """
        return "رقم {}".format(data)

    @staticmethod
    def _validate(text: str) -> None:
        """validate handler input

        Args:
            text (str): input text
        """
        NotEmpty(text)
        isPhone(text)
