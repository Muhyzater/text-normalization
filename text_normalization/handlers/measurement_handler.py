import re

from text_normalization.constants import (
    date_wordList,
    fraction_units,
    plural_fraction_units,
    plural_units,
    units,
)

from . import BaseHandler, number2text, spell_out_number, NotEmpty, isUnit


class MeasuremenHandler(BaseHandler):
    """
    normalize measurements to their full text equivalent
    """

    def _handle(self, ctx: tuple, output: list = None) -> str:
        """handle contexts containing measurements

        Args:
            ctx (tuple): textual context
            output (list, optional): accumulated output. Defaults to None

        Returns:
            str: normalization output
        """
        if output and len(output) > 0:
            last_word = output[-1].split()[-1]
        else:
            last_word = ""
        measurement_block, seprartor = ctx

        if len(measurement_block) > 1:
            measurement_block = "{} {}".format(
                measurement_block[0], measurement_block[1]
            )
        else:
            if len(measurement_block) == 1:
                matches = re.compile("([0-9]+)(.*)")
                matches = matches.match(measurement_block[0])
                if matches:
                    measurement_block = " ".join(matches.groups())
            else:
                measurement_block = "{} {}".format(
                    measurement_block[0], measurement_block[1]
                )

        measurement_block = measurement_block.strip()
        measurements_units = measurement_block.split(".")
        whole_number = measurements_units[0]
        dateFlag = 0
        Date = ""

        # handling for ambiguity between `م` as `متر` the unit
        # and `ميلادي` the calender and other words
        # like `ه`  in `هيرتز` or `هجري`
        # TODO: better handling
        for word in date_wordList:
            if last_word == word:

                numbers_only = [num for num in whole_number if num.isdigit()]
                numbers_only = "".join(numbers_only)

                if whole_number.endswith("هـ"):
                    Date = number2text(numbers_only, 1, 2) + " هجرياً"

                elif whole_number.endswith("ه"):
                    Date = number2text(numbers_only, 1, 2) + " هجرياً"

                elif whole_number.endswith("م"):
                    Date = number2text(numbers_only, 1, 2) + " ميلادياً"

                dateFlag = 1

        measurement_whole_part = ""
        measurement_fraction_part = ""
        measurement_unit = ""

        if len(measurements_units) > 1:

            fraction_number = measurements_units[1]
            fraction_number = fraction_number.replace(" ", "")

            for ind, i in enumerate(fraction_number):
                if i in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                    measurement_fraction_part += i

                else:
                    measurement_unit += fraction_number[ind:]
                    break

            measurement_whole_part = whole_number

        else:

            whole_number = whole_number.replace(" ", "")

            for ind, i in enumerate(whole_number):
                if i in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                    measurement_whole_part += i

                else:
                    measurement_unit += whole_number[ind:]
                    break

        if measurement_unit[-1] in ["²", "2", "³", "3"]:
            abstract_unit = measurement_unit[:-1]

        else:
            abstract_unit = measurement_unit

        if (len(measurement_fraction_part) > 2) or (
            (measurement_unit not in fraction_units)
            and (abstract_unit not in fraction_units)
            and (measurement_fraction_part != "")
        ):

            parsed_values = self.__parse(
                [measurement_whole_part, measurement_fraction_part], measurement_unit
            )

            unit_value = "{} \u0641\u0627\u0635\u0644\u0629 {}".format(
                parsed_values["primaryNumber"],
                spell_out_number(measurement_fraction_part),
            )

            return self._format(unit_value, parsed_values["primaryUnit"])

        else:
            if (
                len(measurement_fraction_part) == 1
                and measurement_fraction_part[0] != "0"
            ):
                measurement_fraction_part += "0"

            unitlist = []
            if dateFlag:
                unitlist += Date.split()
                unitlist = [" ".join(unitlist[0:-1]), "", "", "", unitlist[-1]]

            else:
                parsed_values = self.__parse(
                    [measurement_whole_part, measurement_fraction_part],
                    measurement_unit,
                )

                unitlist.extend(
                    [
                        parsed_values["primaryNumber"],
                        parsed_values["primaryUnit"],
                        parsed_values["secondaryNumber"],
                        parsed_values["secondaryUnit"],
                    ]
                )

            if len(unitlist) == 3:
                unitlist += ["", ""]

            elif len(unitlist) == 4:
                unitlist += [""]

            return self._restore_seprartor(self._format(*unitlist).rstrip(), seprartor)

    @staticmethod
    def _process_ctx_data(ctx: str) -> tuple:
        """process textual data retrived from context

        Args:
            ctx (str): extracted context data

        Returns:
            tuple: measurement values, seprartor
        """
        separator = ""
        if ctx[-1] in [",", "."]:
            separator = ctx[-1]
            ctx = ctx[:-1]
        return ctx.replace("^", "").strip().split(" "), separator

    @staticmethod
    def _format(
        word_name: str = "",
        whole_number: str = "",
        primary_unit: str = "",
        fraction_number: str = "",
        secondary_unit: str = "",
    ) -> str:
        """construct final representation of result

        Args:
            word_name (str, optional): unit_value. Defaults to ''.
            whole_number (str, optional): whole number value. Defaults to ''.
            primary_unit (str, optional): while number unit. Defaults to ''.
            fraction_number (str, optional): fraction number value.
            Defaults to ''.
            secondary_unit (str, optional): fraction number unit.
            Defaults to ''.

        Returns:
            str: formatted result
        """

        if fraction_number == "":
            connector = ""
        else:
            connector = " ﻭ"

        return "{} {} {}{} {} {}".format(
            word_name,
            whole_number,
            connector,
            primary_unit,
            fraction_number,
            secondary_unit,
        )

    @staticmethod
    def __parse(number_parts: list, unit: str) -> dict:
        """parse data retrived from context

        Args:
            number_parts (list): primary and secondary numbers
            unit (str): unit symbol

        Returns:
            dict: primary and secondary values and units
        """
        whole_number = number_parts[0]
        if len(number_parts) == 2:
            fraction_number = number_parts[1]
        else:
            fraction_number = ""

        if unit[-1] in ["²", "2", "³", "3"]:
            if int(whole_number) >= 3 and int(whole_number) <= 10:
                _unit = [plural_units[unit[:-1]], plural_units[unit[-1]]]
            else:
                _unit = [units[unit[:-1]], units[unit[-1]]]

            if fraction_number != "" and unit[:-1] in fraction_units:
                if int(fraction_number) >= 3 and int(fraction_number) <= 10:
                    _fraction_unit = [
                        plural_fraction_units[unit[:-1]],
                        plural_fraction_units[unit[-1]],
                    ]

                else:
                    _fraction_unit = [fraction_units[u] for u in unit]

                _fraction_unit = " ".join(_fraction_unit)

            else:
                _fraction_unit = ""

            return dict(
                primaryNumber=number2text(whole_number),
                primaryUnit=" ".join(_unit),
                secondaryNumber=number2text(fraction_number),
                secondaryUnit=_fraction_unit,
            )

        else:
            if int(whole_number) >= 3 and int(whole_number) <= 10:
                _unit = plural_units[unit]

            else:
                _unit = units[unit]

            if fraction_number != "" and unit in fraction_units:
                if int(fraction_number) >= 3 and int(fraction_number) <= 10:
                    _fraction_unit = plural_fraction_units[unit]

                else:
                    _fraction_unit = fraction_units[unit]

            else:
                _fraction_unit = ""

            return dict(
                primaryNumber=number2text(whole_number),
                primaryUnit=_unit,
                secondaryNumber=number2text(fraction_number),
                secondaryUnit=_fraction_unit,
            )

    @staticmethod
    def _validate(text: str) -> None:
        """validate handler input

        Args:
            text (str): input text
        """
        NotEmpty(text)
        # NOTE `isUnit` validator is breaking on things like "42 كغم"
        # isUnit(text)
