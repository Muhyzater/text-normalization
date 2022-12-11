from text_normalization.generated_files.txtNormListener import txtNormListener
from enum import Enum, unique, auto


@unique
class LexerLabel(Enum):
    """result labels when using `LexerLabeler`"""

    DATE = auto()
    TIME = auto()
    WORD = auto()
    CURRENCY = auto()
    MEASUREMENT = auto()
    IBAN = auto()
    ACCOUNT = auto()
    SEQUENCE_OF_DIGITS = auto()
    EMAIL = auto()
    NUMBER = auto()
    FLOATING_NUM = auto()
    PHONE = auto()
    AR_ACRONYM = auto()
    EN_ACRONYM = auto()
    SYMBOL = auto()


class LexerLabeler(txtNormListener):
    """Label input using ANTLR"""

    result = None

    def exitDate(self, ctx):
        self.result = LexerLabel.DATE

    def exitTime(self, ctx):
        self.result = LexerLabel.TIME

    def exitWord(self, ctx):
        self.result = LexerLabel.WORD

    def exitCurrency(self, ctx):
        self.result = LexerLabel.CURRENCY

    def exitMeasurement(self, ctx):
        self.result = LexerLabel.MEASUREMENT

    def exitIban(self, ctx):
        self.result = LexerLabel.IBAN

    def exitAccount(self, ctx):
        self.result = LexerLabel.ACCOUNT

    def exitSequence_of_digits(self, ctx):
        self.result = LexerLabel.SEQUENCE_OF_DIGITS

    def exitEmail(self, ctx):
        self.result = LexerLabel.EMAIL

    def exitNumber(self, ctx):
        self.result = LexerLabel.NUMBER

    def exitFloating_num(self, ctx):
        self.result = LexerLabel.FLOATING_NUM

    def exitPhone(self, ctx):
        self.result = LexerLabel.PHONE

    def exitAr_acronym(self, ctx):
        self.result = LexerLabel.AR_ACRONYM

    def exitEn_acronym(self, ctx):
        self.result = LexerLabel.EN_ACRONYM

    def exitSymbol(self, ctx):
        self.result = LexerLabel.SYMBOL
