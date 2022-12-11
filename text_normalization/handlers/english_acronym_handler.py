from . import BaseHandler, spell_out_letter


class EnglishAcronymHandler(BaseHandler):
    """
    normalize English acronyms to their full text equivalent
    """

    def _handle(self, ctx: str) -> str:
        """handle contexts containing English acronym

        Args:
            ctx (str): textual context

        Returns:
            str: normalization output
        """
        acronym = ctx
        data = acronym.replace(" ", "").replace(".", "")
        return self._format(spell_out_letter(data))
