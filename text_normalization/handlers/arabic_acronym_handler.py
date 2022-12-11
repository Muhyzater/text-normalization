from text_normalization.constants import ar_acronyms

from . import BaseHandler, spell_out_letter


class ArabicAcronymHandler(BaseHandler):
    """
    normalize Arabic acronyms to their full text equivalent
    """

    def _handle(self, ctx: str) -> str:
        """handle contexts containing Arabic acronyms

        Args:
            ctx (str): textual context

        Returns:
            str: normalization output
        """
        acronym = ctx
        data = acronym.replace(".", "").replace(" ", "")
        return self._format(self.__convert(data))

    @staticmethod
    def __convert(acronym: str) -> str:
        """convert acronym to text if possible

        Args:
            acronym (str): acronym to be converted

        Returns:
            str: acronym full text equivalent
        """
        if acronym in ar_acronyms:
            return ar_acronyms[acronym]
        else:
            return spell_out_letter(acronym)
