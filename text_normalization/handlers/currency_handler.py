import fractions
import re

from text_normalization.constants import (
    currencies,
    fraction_currencies,
    plural_currencies,
    plural_fraction_currencies,
)

from . import (
    BaseHandler,
    number2text,
    spell_out_number,
    NotEmpty,
    isCurrency,
)


class CurrencyHandler(BaseHandler):
    """
    normalize Currency to their full text equivalent
    """

    def _handle(self, ctx: tuple) -> str:
        """handle contexts containing currency
        Args:
            ctx (tuple): textual context
        Returns:
            str: normalization output
        """
        number_parts, currency_unit = ctx
        if len(number_parts) > 2:
            if len(number_parts[2]) > 2 or currency_unit not in fraction_currencies:
                converted = self.__parse(number_parts, currency_unit, fractions=True)
                #fraction = int(number_parts[2]) / (10 ** len(number_parts[2]))
                if "دينار" in converted["primaryCurrency"]:
                    truncated = number_parts[2][0:3]
                else:
                    truncated = number_parts[2][0:2]
                number_parts[2] = truncated
                temp_result = "{} فاصلة {}".format(
                    converted["primaryNumber"], spell_out_number(number_parts[2])
                )

                return self._format(temp_result, converted["primaryCurrency"])

            else:
                if (len(number_parts[2]) == 1) and (number_parts[2][0] != "0"):
                    number_parts[2] += "0"
                return self._format(**self.__parse(number_parts, currency_unit, fractions=True))

        else:
            return self._format(**self.__parse(number_parts, currency_unit))

    @staticmethod
    def _process_ctx_data(ctx: str) -> tuple:
        """process textual data retrived from context

        Args:
            ctx (str): extracted context data

        Returns:
            tuple: number_parts, currency_unit
        """

        tempContext = re.split(r"([0-9]+)|\[\.,\]", ctx)
        tempContext = [x.strip() for x in tempContext if x != ""]

        if tempContext[0].isdigit():
            currency_unit = tempContext[-1]
            number_parts = tempContext[:-1]
        else:
            currency_unit = tempContext[0]
            number_parts = tempContext[1:]

        return number_parts, currency_unit

    @staticmethod
    def _format(
        primaryNumber: str,
        primaryCurrency: str,
        secondaryNumber: str = "",
        secondaryCurrency: str = "",
    ) -> str:
        """construct final representation of result

        Args:
            primaryNumber (str): primary value
            primaryCurrency (str): primary value currency/unit
            secondaryNumber (str, optional): secondary value. Defaults to ''.
            secondaryCurrency (str, optional): secondary value currency/unit.
            Defaults to ''.

        Returns:
            str: formatted result
        """

        if secondaryNumber == "":
            connector = ""
        else:
            connector = " فاصلة"

        return "{} {} {} {}".format(
            primaryNumber,
            connector,
            secondaryNumber,
            primaryCurrency,
        )

    @staticmethod
    def __parse(number_parts: list, unit: str, fractions=False) -> dict:
        """parse data retrived from context

        Args:
            number_parts (list): primary and secondary numbers
            unit (str): currency symbol

        Returns:
            dict: primary and secondary values and currencies
        """
        whole_number = number_parts[0]
        if len(number_parts) == 3:
            fraction_number = number_parts[2]
        else:
            fraction_number = ""

        if int(whole_number) >= 3 and int(whole_number) <= 10 and not fractions:
            _currency = plural_currencies[unit]

        else:
            _currency = currencies[unit]

        if fraction_number != "" and unit in fraction_currencies:
            if int(fraction_number) >= 3 and int(fraction_number) <= 10:
                _fraction = [plural_fraction_currencies[unit]]

            else:
                _fraction = [fraction_currencies[unit]]

            _fraction = " ".join(_fraction)

        else:
            _fraction = ""

        fraction_number = fraction_number.strip("0")
        if fractions and int(whole_number[-1])>2:
            if int(whole_number[-1])>2:
                primary_number = number2text(whole_number, feminine_flag=2)
            else:
                primary_number=number2text(whole_number)
            if int(fraction_number[-1])>2:    
                secondary_number=number2text(fraction_number, feminine_flag=2)
            else:
                secondary_number=number2text(fraction_number)    
        else:
            primary_number=number2text(whole_number)
            secondary_number=number2text(fraction_number)
        return dict(
            primaryNumber=primary_number,
            primaryCurrency=_currency,
            
            secondaryNumber=secondary_number,
            secondaryCurrency=_fraction,
        )

    @staticmethod
    def _validate(text: str) -> None:
        """validate handler input

        Args:
            text (str): input text
        """
        NotEmpty(text)
        isCurrency(text)
