import re
from types import FunctionType

from antlr4 import CommonTokenStream, InputStream, ParseTreeWalker
from text_normalization.generated_files.txtNormLexer import txtNormLexer
from text_normalization.generated_files.txtNormParser import txtNormParser

from . import HandlerValidationException, LexerLabel, LexerLabeler

# ##################################### validators ######################################


def NotEmpty(text: str) -> None:
    """validate if input is not empty"""

    if not text or not text.strip():
        raise HandlerValidationException("empty text!")


def isAlphanumeric(text: str) -> None:
    """validate if input only includes alphanumerics"""

    if re.search(
        r"[^\s\u0621-\u063A\u0641-\u06520-9٠-٩a-z]+",
        text,
        re.UNICODE | re.IGNORECASE,
    ):
        raise HandlerValidationException("can only include alphanumerics!")


def isNumber(text: str) -> None:
    """validate if input only includes numbers"""

    if re.search(r"[^\s0-9٠-٩]+", text):
        raise HandlerValidationException("can only include numbers!")


def isDate(text: str) -> None:
    """validate if input is a valid date string"""

    if not __get_lexer_label(text) == LexerLabel.DATE:
        raise HandlerValidationException("invalid date string!")


def isTime(text: str) -> None:
    """validate if input is a valid time string"""

    if not __get_lexer_label(text) == LexerLabel.TIME:
        raise HandlerValidationException("invalid time string!")


def isUnit(text: str) -> None:
    """validate if input is a valid unit string"""

    if not __get_lexer_label(text) == LexerLabel.MEASUREMENT:
        raise HandlerValidationException("invalid unit string!")


def isCurrency(text: str) -> None:
    """validate if input is a valid currency string"""

    if not __get_lexer_label(text) == LexerLabel.CURRENCY:
        raise HandlerValidationException("invalid currency string!")


def isPhone(text: str) -> None:
    """validate if input is a valid Phone string"""

    if not __get_lexer_label(text) == LexerLabel.PHONE:
        raise HandlerValidationException("invalid phone string!")


# ####################################### utils ########################################


def __get_lexer_label(text: str) -> LexerLabel:
    """label `text` using ANTLR logic

    Args:
        text (str): text to be labeled

    Returns:
        LexerLabel: label Enum value
    """
    labeler = LexerLabeler()

    ParseTreeWalker().walk(
        labeler,
        txtNormParser(
            CommonTokenStream(txtNormLexer(InputStream(" " + text + " ")))
        ).text(),
    )
    return labeler.result
