from text_normalization.constants import ar_alphabet, symbols, units

from . import BaseHandler


class SymbolHandler(BaseHandler):
    """
    normalize symbols to their full text equivalent
    """

    def _handle(self, ctx: str) -> str:
        """handle contexts containing symbols

        Args:
            ctx (str): textual context

        Returns:
            str: normalization output
        """
        return self.__convert(ctx)

    @staticmethod
    def __convert(symbol: str) -> str:
        """convert symbols to their text equivalents

        Args:
            symbol (str): symbol to be converted

        Returns:
            str: text equivalent
        """
        if symbol in symbols:
            return symbols[symbol]

        elif symbol in ar_alphabet:
            return ar_alphapet[symbol]

        elif symbol in units:
            return units[symbol]

        else:
            return symbol
