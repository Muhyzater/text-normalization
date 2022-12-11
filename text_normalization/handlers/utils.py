import logging

import pyarabic.number as all_numbers
import requests
from flask import g
from text_normalization.constants import (
    ar_alphabet,
    cardinal,
    diacritized_ar_alphabet,
    diacritized_cardinal,
    diacritized_eng_chars_in_arabic,
    eng_chars_in_arabic,
    indic2latin,
)


def number2text(num: str, feminine_flag: int = 1, grammar_pos_flag: int = 1) -> str:
    """
    Uses PyArabic library to convert numbers into arabic text.

    Parameters:
    ----------
    num: string
            Number to be textualized

    feminine_flag: int
            Gender of counted object (1 for masculine & 2 for feminine)
            Default is 1

    grammar_pos_flag: int
            Grammar position of counted object (1 if Marfoua & 2 if Mansoub or
            Majrour)
            Default is 1

    Returns:
    -------
            Arabic text of num.
    """
    if num == "":
        return ""
    arn = all_numbers.ArNumbers()
    arn.set_feminine(feminine_flag)
    arn.set_format(grammar_pos_flag)

    return arn.int2str(num).replace(" و ", " و")


def spell_out_number(number: str, use_diacritized: bool = False) -> str:
    """convert individual number digits to their textual cardinal equivalent

    Args:
        number (str): numerical number
        use_diacritized (bool, optional): if True use diacritized text in
        result. Defaults to False.
    Returns:
        str: cardinal equivalent
    """
    if use_diacritized:
        used_cardinal = diacritized_cardinal
    else:
        used_cardinal = cardinal

    tmp = []
    for i in number:
        if i in cardinal:
            tmp.append(used_cardinal[i])
        elif i in indic2latin:
            tmp.append(used_cardinal[indic2latin[i]])
        else:
            pass

    return " ".join(tmp)


def spell_out_letter(text: str, use_diacritized: bool = False) -> str:
    """convert individual charecters (English and Arabic) to their
    textual equivalent

    Args:
        text (str): text to be spelled about
        use_diacritized (bool, optional): if True use diacritized text in
        result. Defaults to False.
    Returns:
        str: textual equivalent
    """

    # string is empty or just spaces
    if not text.strip():
        return ""

    if use_diacritized:
        used_ar_alphabet = diacritized_ar_alphabet
        used_eng_chars_in_arabic = diacritized_eng_chars_in_arabic

    else:
        used_ar_alphabet = ar_alphabet
        used_eng_chars_in_arabic = eng_chars_in_arabic

    result = []
    for char in text.lower():
        if char in used_ar_alphabet:
            result.append(used_ar_alphabet[char])

        elif char in used_eng_chars_in_arabic:
            result.append(used_eng_chars_in_arabic[char])

        elif char != " ":
            result.append(char)

    return " ".join(result)


def diacritize_text(text: str, url: str, use_external: bool) -> str:
    """use Tashkeel service to diacritize text,
    if it failed to it returns `text`

    Args:
        text (str): text to diacritize
        url (str): Tashkeel service endpoint
        use_external (bool): request external using the `requests` package

    Returns:
        str: diacritized text
    """
    result = text
    response = None

    try:
        if use_external:
            response = requests.post(url=url, json={"text": text})

        else:
            response = g.call_microservice("post", url=url, json={"text": text})

    except Exception as e:
        logging.error(e)

    if response and response.ok:
        result = response.json()["results"]["text"]

    else:

        _error = "graciously continuing without it"

        # error response are falsy
        if response is not None:
            _error = "error : {} {}".format(response.status_code, response.reason)

        logging.info("Tashkeel did not respond properly, {}".format(_error))

    return result


if __name__ == "__main__":
    print(spell_out_number("123"))
    print(number2text("123"))
    print(spell_out_letter("ذهب الولد الى الحديقة"))

    print(">>>> with use_diacritized <<<<")

    print(spell_out_number("123", use_diacritized=True))
    print(spell_out_letter("ذهب الولد الى الحديقة", use_diacritized=True))
