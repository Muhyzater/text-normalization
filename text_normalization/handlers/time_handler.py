import text_normalization.constants as constants

from . import BaseHandler, number2text, NotEmpty, isTime


class TimeHandler(BaseHandler):
    """
    normalize time to their full text equivalent
    """

    def _handle(self, ctx: tuple) -> str:
        """handle contexts containing time

        Args:
            ctx (tuple): textual context

        Returns:
            str: normalization output
        """
        timeParts, timeUnit = ctx
        parsed_t = self.__convert_time(timeParts, timeUnit)

        return self._format(parsed_t, parsed_t[4])

    @staticmethod
    def _get_ctx_data(ctx) -> tuple:
        """extract data needed for text normalization from context

        Args:
            ctx (object): textual context

        Returns:
            tuple: timeParts, timeUnit
        """
        return ctx.TIME_BULK().getText()

    def _process_ctx_data(self, ctx: str) -> tuple:
        """process textual data retrived from context

        Args:
            ctx (str): extracted context data

        Returns:
            tuple: timeParts, timeUnit
        """
        WHITE_LISTED_MARK = [
            "!",
            "؟",
            "?",
            "(",
            ")",
            "{",
            "}",
            "<",
            ">",
            "[",
            "]",
            '"',
            "'",
            "؛",
            ",",
            "،",
            ";",
            "`",
            "‘",
            "~",
            "|",
            "’",
            ".",
        ]

        for mark in WHITE_LISTED_MARK:
            if mark in ctx:
                ctx = ctx.replace(mark, "")

        ctx, timeUnit = self.__get_time_of_day(ctx)
        timeParts = [int(i) for i in ctx.split(":")]

        return timeParts, timeUnit

    def __convert_time(self, t: list, u: str = None) -> list:
        """
        Parameters:
        ----------
        t: list(string)
                a list including HH, MM, and SS if available.
        u: string
                time unit if available
        minutes_style boolean:
                False: Express the minutes in numbers ﺎﻟﻭﺎﺣﺩﺓ ﻮﺛﻼﺛﻮﻧ ﺪﻘﻴﻗﺓ
                True: use special names ﺎﻟﻭﺎﺣﺩﺓ ﻭﺎﻠﻨﺼﻓ

        Returns:
        -------
        list (string)
                the time expressed in pronouncable words
        """
        tmp_time = []
        if u and t[0] == 12 and u.lower() == "am":
            t[0] = 0  # am

        if t[1] in [40, 45, 50, 55]:
            # t[0] += 1 # 9:45 = ﺎﻠﻋﺎﻠﺷﺭﺓ ﺇﻻ ﺮﺒﻋ

            # 9:45 = ﺎﻠﻋﺎﻠﺷﺭﺓ ﺇﻻ ﺮﺒﻋ
            tmp_time.append(self.__convert_hours(t[0] + 1))
        else:
            tmp_time.append(self.__convert_hours(t[0]))

        if t[1] in constants.special_minutes:
            tmp_time.append(" " + constants.special_minutes[t[1]])
            tmp_time.append("")  # place holder for seconds
            if u is None:
                addition = "صباحاً" if t[0] < 12 else "مساءً"
                tmp_time.append(addition)
            else:
                addition = "صباحاً" if u.lower() == "am" else "مساءً"
                tmp_time.append(addition)
                """
                if u.lower() == "pm" and t[0] < 12:
                    tmp_time.append(constants.am_pm[str(t[0] + 12)])
                else:
                    tmp_time.append(constants.am_pm[str(t[0])])
                """
            tmp_time.append(2)  # place the tamyeez after the seconds
        else:
            tmp_time.append(self.__convert_min_sec(t[1], 2))
            if len(t) > 2:
                tmp_time.append(self.__convert_min_sec(t[2], 1))
            else:
                tmp_time.append("")  # place holder for seconds
            if u is None:
                addition = "صباحاً" if t[0] < 12 else "مساءً"
                tmp_time.append(addition)
            else:
                addition = "صباحاً" if u.lower() == "am" else "مساءً"
                tmp_time.append(addition)
            tmp_time.append(0)  # place the tamyeez after the hours

        return tmp_time

    def __convert_min_sec(self, num: int, sec_min: int = 1) -> str:
        """
        sec -> 1
        min -> 2
        """

        tmp = " "

        if num == 0:
            pass
        elif num < 3 and num > 0:
            tmp += "و"
        else:
            tmp += "و"
            # str -> int -> str to remove any zeros to the left

            tmp += number2text(str(num))
            tmp += " "

        tmp += self.__get_tamyeez(num, sec_min)
        return tmp

    @staticmethod
    def _format(value: list, tamyeez_position: int) -> str:
        """construct final representation of result

        Args:
            value (str): time values
            tamyeez_position (int):insert the tamyeez after
            value[tamyeez_position]

        Returns:
            str: formatted result
        """
        value[tamyeez_position] += " " + value[3]
        return "{}{}{}".format(value[0], value[1], value[2]).rstrip()

    @staticmethod
    def __get_time_of_day(timeBulk: str) -> tuple:
        """determine if the time falls under 'AM' or 'PM' and remove them
        from text

        Args:
            timeBulk (str): time text data

        Returns:
            tuple: timeBulk, timeUnit
        """
        AMs = [
            "\u0635\u0628\u0627\u062D\u0627\u064B",
            "\u0635\u0628\u0627\u062D\u0627",
            "\u0635",
            "am",
            "AM",
        ]
        PMs = [
            "\u0645\u0633\u0627\u0621\u064B",
            "\u0645\u0633\u0627\u0621",
            "\u0645",
            "\uFEE1",
            "pm",
            "PM",
        ]

        timeUnit = None
        for a in AMs:
            if a in timeBulk:
                timeUnit = "am"
                timeBulk = (timeBulk.replace(a, "")).rstrip()
                break

        if timeUnit is None:
            for p in PMs:
                if p in timeBulk:
                    timeUnit = "pm"
                    timeBulk = timeBulk.replace(p, "").rstrip()
                    break
        return timeBulk, timeUnit

    @staticmethod
    def __convert_hours(hrs: int) -> str:
        """convert numbered hours to their text equivalent

        Args:
            hrs (int): numbered hours

        Returns:
            str: text equivalent
        """
        if hrs > 12:
            hrs -= 12  # stick to 12 hour format

        if hrs == 0:
            return "الثانية عشرة"  # am
        elif hrs == 1:
            return "الواحدة"
        elif hrs == 11:
            return "الحادية عشرة"
        elif hrs == 12:
            return "الثانية عشرة"  # pm
        else:
            return constants.ordinal[str(hrs)] + "ة"

    @staticmethod
    def __get_tamyeez(num: int, time_unit: int = 1) -> str:
        """
        Returns the proper tamieez for the given number

        Parameters:
        -----------
        num int:
                the number to which a tamyeez is required.
        time_unit int:
                a flag specifing whether num represents an hour, a minute or a
                            second
                1 -> second
                2 -> minute
                3 -> hour

        Returns:
        --------
        tamyeez string
        """

        if num == 0:
            return ""

        elif num == 1:
            if time_unit == 1:
                return "ثانية واحدة"
            elif time_unit == 2:
                return "دقيقة واحدة"
            elif time_unit == 3:
                return "ساعة واحدة"

        elif num == 2:
            if time_unit == 1:
                return "ثانيتان"
            elif time_unit == 2:
                return "دقيقتان"
            elif time_unit == 3:
                return "ساعتان"

        elif num > 2 and num < 11:
            if time_unit == 1:
                return "ثوان"
            elif time_unit == 2:
                return "دقائق"
            elif time_unit == 3:
                return "ساعات"

        else:
            if time_unit == 1:
                return "ثانية"
            elif time_unit == 2:
                return "دقيقة"
            elif time_unit == 3:
                return "ساعة"

    @staticmethod
    def _validate(text: str) -> None:
        """validate handler input

        Args:
            text (str): input text
        """
        NotEmpty(text)
        isTime(text)
