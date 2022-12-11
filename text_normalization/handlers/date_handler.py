import re

from text_normalization.constants import (
    dating_list,
    hijriMonth,
    hundreds,
    month_wordlist,
    months,
    ordinal,
    tens,
    the_first,
    thousands,
)

from . import BaseHandler, number2text, NotEmpty, isDate


class DateHandler(BaseHandler):
    """
    normalize dates to their full text equivalent
    """

    def _handle(self, ctx: str, output: list = None) -> str:
        """handle contexts containing dates

        Args:
            ctx (str): textual context
            output (list, optional): accumulated output. Defaults to None

        Returns:
            str: normalization output
        """

        Date = {"day": "", "month": "", "year": "", "dating": "", "token": None}

        if output and len(output) > 0:
            last_word = output[-1].split()[-1]
        else:
            last_word = ""
        rawDateBulk = ctx

        tempRawDateBulk = re.split(r"/|\-|\ |([0-9]+)", rawDateBulk)
        tempRawDateBulk = [
            x.strip()
            for x in tempRawDateBulk
            if (x and x.isdigit() or x in month_wordlist or x in dating_list)
        ]

        if tempRawDateBulk[-1] == "هـ":
            Date["dating"] = " هجرياً"
            tempRawDateBulk = tempRawDateBulk[:-1]
        elif tempRawDateBulk[-1] == "ه":
            Date["dating"] = " هجرياً"
            tempRawDateBulk = tempRawDateBulk[:-1]
        elif tempRawDateBulk[-1] == "م":
            Date["dating"] = " ميلادياً"
            tempRawDateBulk = tempRawDateBulk[:-1]

        if len(tempRawDateBulk) == 3:
            year = tempRawDateBulk[2]
            if year.isdigit():
                Date["year"] = year
            tempRawDateBulk = tempRawDateBulk[:-1]

        if len(tempRawDateBulk) == 2:
            m_or_y = tempRawDateBulk[1]
            if m_or_y.isdigit():
                if last_word == "شهر":
                    Date["month"] = m_or_y
                else:
                    if Date["year"] != "":
                        Date["month"] = m_or_y
                    elif len(m_or_y) > 2:
                        Date["year"] = m_or_y
                    else:
                        Date["month"] = m_or_y
            elif m_or_y in month_wordlist:
                Date["month"] = m_or_y
            tempRawDateBulk = tempRawDateBulk[:-1]

        if len(tempRawDateBulk) == 1:
            d_or_m_or_y = tempRawDateBulk[0]
            if d_or_m_or_y in month_wordlist:
                Date["month"] = d_or_m_or_y
            else:
                if len(d_or_m_or_y) >= 3:
                    Date["year"] = d_or_m_or_y
                else:
                    Date["day"] = d_or_m_or_y

        Date["day"] = self.__convert_days(Date["day"]) if Date["day"] else ""

        Date["month"] = (
            self.__convert_months(Date["month"], Date["dating"])
            if Date["month"]
            else ""
        )

        Date["year"] = number2text(Date["year"], 1, 2) if Date["year"] else ""

        if last_word in {"شهر", "سنة", "عام"}:
            Date["token"] = last_word

        return self._format(Date)

    @staticmethod
    def _get_ctx_data(ctx) -> str:
        """extract data needed for text normalization from context

        Args:
            ctx (object): textual context

        Returns:
            str: extracted date data
        """
        return ctx.DATE_BULK().getText()

    @staticmethod
    def _format(data: dict) -> str:
        """construct final representation of result

        Args:
           data (dict): contains year month and day data

        Returns:
            str: formatted result
        """

        if data.get("day") and data.get("month") and data.get("year"):
            return "{} من {} عام {} {}".format(
                data.get("day"), data.get("month"), data.get("year"), data.get("dating")
            )

        elif data["day"] and data["month"]:
            return "{} من {}".format(data["day"], data["month"])

        elif data["month"] and data["year"]:
            return "{} من  عام {} {}".format(
                data["month"], data["year"], data["dating"]
            )
        elif data["year"]:
            if data["token"]:
                return "{} {}".format(data["year"], data["dating"])
            else:
                return "عام {} {}".format(data["year"], data["dating"])

        else:
            return ""

    @staticmethod
    def __convert_days(days_in_num: str) -> str:
        """convert numbered days to their ordinal text equivalents

        Args:
            days_in_num (str): day to be converted

        Returns:
            str: ordinal equivalent
        """
        day = int(days_in_num)
        if day == 1:
            return the_first
        elif day < 10 and day > 1:
            # converting from str -> int -> str gets rid of leading zeros
            return ordinal[str(day)]
        elif day == 10:
            return ordinal[days_in_num]
        elif day > 10 and day < 20:
            return ordinal[days_in_num[1]] + " " + tens["1"]
        elif day in [20, 30]:
            return ordinal[days_in_num[1]] + " ال" + tens[days_in_num[0]]
        else:
            return ordinal[days_in_num[1]] + " وال" + tens[days_in_num[0]]

    @staticmethod
    def __convert_months(month_in_num: str, dateType: str = "ميلادياً") -> str:
        """convert numbered months to their named equivalent

        Args:
            month_in_num (str): numbered month
            dateType (str, optional): calander type. Defaults to "ميلادياً".

        Returns:
            str: oridinal equivalent
        """
        if len(month_in_num) > 2:  # The month is already text not number
            return month_in_num
        else:
            if "هجرياً" in dateType:
                return hijriMonth[int(month_in_num)]
            else:
                return months[int(month_in_num)]

    @staticmethod
    def _validate(text: str) -> None:
        """validate handler input

        Args:
            text (str): input text
        """
        NotEmpty(text)
        isDate(text)
