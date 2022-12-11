from collections import namedtuple

from grpc import StatusCode


class Sentence:
    """
    Packages the sentence with the attributes necessary for normalization
    """

    def __init__(self, text, last_dot=None, numbers=None):
        self.text = text
        self.last_dot = last_dot
        self.numbers = numbers


class Diacritizations:
    """[summary]

    Args:
        Enum ([type]): [description]
    """

    FATHA = u"\u064e"
    DAMMA = u"\u064f"
    KASRA = u"\u0650"
    TANWEEN_FATH = u"\u064B"
    TANWEEN_DAMM = u"\u064C"
    TANWEEN_KASR = u"\u064D"
    MAJROOR_MANSOOB = (FATHA, KASRA, TANWEEN_FATH, TANWEEN_KASR)
    MARFOU = (DAMMA, TANWEEN_DAMM)


class SSMLParsingException(Exception):
    pass


class StatusCodeMapper(object):
    """
    Mapper to map status to its REST or RPC equivalent
    """

    def __init__(self, use_rpc):
        self.use_rpc = use_rpc

    @property
    def OK(self):
        return StatusCode.OK if self.use_rpc else 200

    @property
    def INVALID_ARGUMENT(self):
        return StatusCode.INVALID_ARGUMENT if self.use_rpc else 400

    @property
    def INTERNAL(self):
        return StatusCode.INTERNAL if self.use_rpc else 500

    @property
    def OUT_OF_RANGE(self):
        return StatusCode.OUT_OF_RANGE if self.use_rpc else 413


Processed = namedtuple("Processed", ["response", "code", "headers"])

# expose
from .base_step import BaseStep  # nopep8
from .digit_conversion import DigitConversion  # nopep8
from .gender_pos import NormalizeGenderPos  # nopep8
from .normalize_phone_numbers import NormalizePhoneNumbers  # nopep8
from .packaging import Packaging  # nopep8
from .split_text import SplitText  # nopep8
from .ssml_parsing import SSMLParsing  # nopep8
from .tree_walking import TreeWalking  # nopep8
