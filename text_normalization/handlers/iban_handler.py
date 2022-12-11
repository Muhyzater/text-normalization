from text_normalization.constants import eng_chars_in_arabic

from . import (
    BaseHandler,
    NotEmpty,
    isAlphanumeric,
    number2text,
    spell_out_number,
)


class IbanHandler(BaseHandler):
    """
    normalize IBANs to their full text equivalent
    """

    def _handle(self, ctx: str) -> str:
        """handle contexts containing IBANs

        Args:
            ctx (str): textual context

        Returns:
            str: normalization output
        """

        # JO71CBJO0000000000001234567890
        iban = ctx
        return " ".join(self.__convert(iban))

    @staticmethod
    def _process_ctx_data(ctx: str) -> str:
        """process textual data retrived from context

        Args:
            ctx (str): extracted context data

        Returns:
            str: processed context data
        """
        return ctx.replace(" ", "").replace(",", "")

    @staticmethod
    def __convert(iban: str) -> str:
        """convert acronym to text if possible

        Args:
            acronym (str): acronym to be converted

        Returns:
            str: acronym full text equivalent
        """

        normalized_text = []
        for c in iban.lower():
            if c in eng_chars_in_arabic:
                normalized_text.append(eng_chars_in_arabic[c])
            elif c.isdigit():
                normalized_text.append(spell_out_number(c))
            else:
                normalized_text.append(c)
        return normalized_text

    @staticmethod
    def _validate(text: str) -> None:
        """validate handler input

        Args:
            text (str): input text
        """
        NotEmpty(text)
        isAlphanumeric(text)
