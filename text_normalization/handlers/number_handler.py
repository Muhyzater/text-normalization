from text_normalization.constants import date_keywords, months

from . import BaseHandler, number2text, spell_out_number


class NumberHandler(BaseHandler):
    """
    normalize numbers to their full text equivalent
    """

    def _handle(self, ctx: str, output: list = None, advanced: bool = False) -> str:
        """handle contexts containing numbers

        Args:
            ctx (str): textual context
            output (list, optional): accumulated output. Defaults to None
            advanced (bool, optional): should the advanced options be applied.
            Defaults to False.

        Returns:
            str: normalization output
        """

        num = ctx

        # handle cases where number is very long which causes an exception in pyarabic
        if len(num) > 12:
            return num.replace("-", ""), spell_out_number(num)

        # handle date ambiguity like :
        # بشهر 5
        # عام 1990
        if output and len(output) > 0:
            last_word = output[-1].split()[-1]
        else:
            last_word = ""

        if last_word in date_keywords:
            if "شهر" in last_word:
                month = months.get(int(num))
                if month:
                    word_output = month
                else:
                    word_output = number2text(num.replace("-", ""), 1, 2)
            elif int(num[0]) in range(1, 3):
                word_output = number2text(num.replace("-", ""), 1, 2)
            else:
                word_output = number2text(num.replace("-", ""), 2, 2)

            return num.replace("-", ""), word_output

        if advanced:
            if int(num) < 0:
                word_output = num.replace("-", "سالب ")
            else:
                word_output = num
        else:
            if int(num) < 0:
                word_output = "سالب " + number2text(num.replace("-", ""))
            else:
                word_output = number2text(num)

        return num.replace("-", ""), word_output
