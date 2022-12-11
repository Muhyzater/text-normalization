import re

from . import BaseHandler, number2text, spell_out_number


class FloatingPointHandler(BaseHandler):
    """
    normalize floating point numbers to their full text equivalent
    """

    def _handle(self, ctx: tuple) -> str:
        """handle contexts containing floating point numbers

        Args:
            ctx (tuple): textual context

        Returns:
            str: normalization output
        """
        primary, fraction, is_negtive = ctx
        primary = number2text(primary, 1)

        if (fraction[0] in ["0", "\u0660"]) or len(fraction) > 3:
            secondary = spell_out_number(fraction)
        else:
            secondary = number2text(fraction, 1)

        if is_negtive:
            primary = "سالب " + primary

        return self._format(primary, secondary)

    @staticmethod
    def _process_ctx_data(ctx: str) -> tuple:
        """process textual data retrived from context

        Args:
            ctx (str): extracted context data

        Returns:
            tuple: primary, fraction, is_negtive
        """
        is_negtive = float(ctx.replace(" ", "").replace(",", "")) < 0

        if ctx.startswith("-") or ctx.startswith("-"):
            ctx = ctx[1:]
        ctx = re.split(r"\.|,", ctx)
        primary = ctx[0]
        fraction = ctx[1]

        return primary, fraction, is_negtive

    @staticmethod
    def _format(primary: str, secondary: str) -> str:
        """construct final representation of result

        Args:
            primary (str): primary value
            secondary (str): fraction value

        Returns:
            str: formatted result
        """
        return "{} \u0641\u0627\u0635\u0644\u0629 {}".format(primary, secondary)
