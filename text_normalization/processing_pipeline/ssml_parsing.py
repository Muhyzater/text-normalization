import re
import xml.etree.ElementTree as ET

import text_normalization.handlers as rule_handlers
from pyarabic.number import number2ordinal
from text_normalization.handlers import (
    diacritize_text,
    number2text,
    spell_out_letter,
    spell_out_number,
    HandlerValidationException,
    NotEmpty,
    isAlphanumeric,
    isNumber,
)

from . import BaseStep, Processed, SSMLParsingException, StatusCodeMapper


class SSMLParsing(BaseStep):
    """
    Parse and evaluate SSML tags in text
    """

    def __init__(self, use_rpc: bool):

        self._code_mapper = StatusCodeMapper(use_rpc)

        patterns = [
            "(<{tag}[^<]*</{tag}>)".format(tag=tag) for tag in ("say-as", "sub")
        ]

        self.tags = re.compile("|".join(patterns))

    def process(self, request: dict, config: dict):

        if not request["parse_ssml"]:

            return self.process_next(request, config)

        if not self.__is_valid_XML(request["text"]):
            return Processed(
                response="invalid SSML: bad XML",
                code=self._code_mapper.INVALID_ARGUMENT,
                headers=None,
            )

        try:
            text = self.__parse(
                request["text"], config["tashkeel_url"], config["use_rpc"]
            )

            return Processed(response=text, code=self._code_mapper.OK, headers=None)

        except SSMLParsingException as e:

            return Processed(
                response=e.args[0],
                code=self._code_mapper.INVALID_ARGUMENT,
                headers=None,
            )

    def __parse(self, ssml_text: str, taskeel_url: str, use_external: bool) -> str:
        """parse text containg SSML tags and evaluate `say-as` and `sub` tags

        Args:
            ssml_text (str): SSML text
            taskeel_url (str): endpoint to Tashkeel service
            use_external (bool): request external using the `requests` package

        Returns:
            str: parsed and evaluated SSML

        Raises:
            SSMLParsingException

        """

        def say_as_tag_handler(node) -> str:

            if "interpret-as" not in node.attrib:
                raise SSMLParsingException(
                    "missing attribute 'interpret-as' from 'say-as' tag"
                )

            handlers = dict(
                cardinal=self.__cardinal_handler,
                ordinal=self.__ordinal_handler,
                characters=self.__spell_out,
                date=rule_handlers.DateHandler.handle,
                phone=rule_handlers.PhoneHandler.handle,
                iban=rule_handlers.IbanHandler.handle,
                currency=rule_handlers.CurrencyHandler.handle,
                time=rule_handlers.TimeHandler.handle,
                unit=rule_handlers.MeasuremenHandler.handle,
            )

            interpretation = node.attrib["interpret-as"].strip().lower()
            text = node.text

            if interpretation not in handlers:
                raise SSMLParsingException(
                    "invalid 'interpret-as' attribute value: {}. "
                    "possible values: {}".format(interpretation, list(handlers.keys()))
                )
            try:
                result = handlers[interpretation](text)
            except HandlerValidationException as e:
                raise SSMLParsingException(
                    "Error handling `say-as` tag: {}".format(e.args[0])
                )

            if interpretation not in ["characters"]:
                result = diacritize_text(result, taskeel_url, use_external)
            return result

        def sub_tag_handler(node) -> str:
            return node.attrib.get("alias", node.text)

        def handler(match) -> str:

            # parse xml for better handling
            try:
                node = ET.fromstring(match.group())
            except ET.ParseError as e:
                raise SSMLParsingException("invalid SSML format")

            if node.tag == "say-as":
                result = say_as_tag_handler(node)

            else:
                result = sub_tag_handler(node)

            return " " + result + " "

        return re.sub(r"\s+", " ", self.tags.sub(handler, ssml_text)).strip()

    @staticmethod
    def __spell_out(text: str) -> str:
        """spell out each charecter in text, either Arabic, English or numbers

        Args:
            text (str): text to be spelt

        Returns:
            str: spelt text
        """
        NotEmpty(text)
        isAlphanumeric(text)

        result = []

        for char in text:

            number = spell_out_number(char, use_diacritized=True)
            if number:
                result.append(number)
            else:
                result.append(spell_out_letter(char, use_diacritized=True))

        return " ".join(result)

    @staticmethod
    def __is_valid_XML(text: str) -> bool:
        """validate that `text` is a valid XML

        Args:
            text (str): text to be validated

        Returns:
            bool: is valid XML
        """
        try:
            ET.fromstring(text)
        except ET.ParseError:
            return False

        return True

    @staticmethod
    def __ordinal_handler(text: str) -> str:
        """get textual equivalent for ordinal numbers

        Args:
            text (str): input string

        Returns:
            str: textual equivalent
        """
        NotEmpty(text)
        isNumber(text)
        return number2ordinal(text)

    @staticmethod
    def __cardinal_handler(text: str) -> str:
        """get textual equivalent for cardinal numbers

        Args:
            text (str): input string

        Returns:
            str: textual equivalent
        """
        NotEmpty(text)
        isNumber(text)
        return number2text(text)
