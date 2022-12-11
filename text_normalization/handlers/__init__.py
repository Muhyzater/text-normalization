from .utils import *
from .lexer_labeler import LexerLabeler, LexerLabel


class HandlerValidationException(Exception):
    """custom exception for invalid input to handlers"""

    pass


from .validators import *  # nopep8

# expose handlers
from .base_handler import BaseHandler  # nopep8
from .number_handler import NumberHandler as number  # nopep8
from .phone_handler import PhoneHandler as phone  # nopep8
from .arabic_acronym_handler import ArabicAcronymHandler as arabic_acronym  # nopep8
from .english_acronym_handler import EnglishAcronymHandler as english_acronym  # nopep8
from .date_handler import DateHandler as date  # nopep8
from .time_handler import TimeHandler as time  # nopep8
from .currency_handler import CurrencyHandler as currency  # nopep8
from .measurement_handler import MeasuremenHandler as measurement  # nopep8
from .iban_handler import IbanHandler as iban  # nopep8
from .account_number_handler import AccountNumberHandler as account  # nopep8
from .sequence_of_digits_handler import (
    SequenceOfDigitsHandler as sequenceOfDigits,
)  # nopep8
from .floating_point_handler import FloatingPointHandler as floating_point  # nopep8
from .symbol_handler import SymbolHandler as symbol  # nopep8

# create handlers
ArabicAcronymHandler = arabic_acronym()
EnglishAcronymHandler = english_acronym()
PhoneHandler = phone()
DateHandler = date()
TimeHandler = time()
CurrencyHandler = currency()
MeasuremenHandler = measurement()
IbanHandler = iban()
AccountNumberHandler = account()
SequenceOfDigitsHandler = sequenceOfDigits()
NumberHandler = number()
FloatingPointHandler = floating_point()
SymbolHandler = symbol()
