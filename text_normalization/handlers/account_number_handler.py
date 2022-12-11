from . import BaseHandler, spell_out_number


class AccountNumberHandler(BaseHandler):
    """
    normalize Account numbers to their full text equivalent
    """

    def _handle(self, ctx: str) -> str:
        """handle contexts containing Account numbers

        Args:
            ctx (str): textual context

        Returns:
            str: normalization output
        """

        # 4 digits branch number /
        # 7 digits customer number /
        # 3 digits account currency code /
        # 4 digits account ledger code /
        # 3 digits account sub sequence for this ledger
        # 0123/0123456/001/1111/000

        account_number = ctx
        branch_number = spell_out_number(account_number[0:4])
        customer_number = spell_out_number(account_number[5:12])
        account_currency_code = spell_out_number(account_number[13:16])
        account_ledger_code = spell_out_number(account_number[17:21])
        account_sub_sequence = spell_out_number(account_number[22:25])

        return self._format(
            branch_number,
            customer_number,
            account_currency_code,
            account_ledger_code,
            account_sub_sequence,
        )

    @staticmethod
    def _format(
        branch_number: str,
        customer_number: str,
        account_currency_code: str,
        account_ledger_code: str,
        account_sub_sequence: str,
    ) -> str:
        """construct final representation of result

        Args:
            word_name (str): unit_value.
            whole_number (str): whole number value.
            primary_unit (str): while number unit.
            fraction_number (str): fraction number value.
            secondary_unit (str): fraction number unit.

        Returns:
            str: formatted result
        """

        return "{} {} {} {} {}".format(
            branch_number,
            customer_number,
            account_currency_code,
            account_ledger_code,
            account_sub_sequence,
        )
