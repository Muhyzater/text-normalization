import logging

import pyarabic.number as number
import requests
from flask import g
from text_normalization.handlers import number2text

from . import BaseStep, Diacritizations

POS_Name_Tags = [
    "DFAJ",
    "DFN",
    "DMAJ",
    "DMN",
    "FWN",
    "PFAJ",
    "PFN",
    "PIAJ",
    "PIN",
    "PMAJ",
    "PMN",
    "SFAJ",
    "SFN",
    "SMAJ",
    "SMN",
    "PN",
]
arn = number.ArNumbers()


class NormalizeGenderPos(BaseStep):
    """
    Uses gender detection and tashkeel models
    to normalize numbers in the advanced mode
    """

    def process(self, request: dict, config: dict):

        self.config = config

        for sentence in request["sentences"]:

            sentence.text = sentence.text.strip()

            if request["advanced"]:
                sentence.text = self.normalize_gender_and_grammatical_pos(
                    sentence.text, sentence.numbers
                )

        return self.process_next(request, config)

    def diacritize(self, text):
        try:
            tashkeel_url = self.config.get("tashkeel_url", None)

            if self.config["use_rpc"]:
                r = requests.post(url=tashkeel_url, json={"text": text})
            else:
                r = g.call_microservice("post", url=tashkeel_url, json={"text": text})
            result = r.json()
            tashkeel_res = result["results"]["text"]
        except Exception as e:
            logging.error(e)

            return text

        return tashkeel_res

    def normalize_gender_and_grammatical_pos(self, normalized_txt, numbers):
        if normalized_txt == "" or normalized_txt is None:
            return normalized_txt
        words = normalized_txt.split()
        numbers_indecies = []
        original_numbers = []
        for i, v in enumerate(words):
            number = ""
            grammar_flag = 1  # grammer format 1 or 2 to add ين or ون
            if v in numbers:
                numbers_indecies.append(i)
                original_numbers.append(v)
                if int(v) > 1:
                    words[i] = "تفكير"
        if len(numbers_indecies) == 0:
            return normalized_txt
        tmp_sentence = " ".join(words)
        tashkel_res = self.diacritize(tmp_sentence)
        tashkel_res = tashkel_res.split(" ")

        for ind, i in enumerate(numbers_indecies):
            last_char = tashkel_res[i][len(tashkel_res[i]) - 1]

            if last_char in Diacritizations.MARFOU:
                # مرفوع
                grammar_flag = 1

            elif last_char in Diacritizations.MAJROOR_MANSOOB:
                # مجرور أو منصوب
                grammar_flag = 2

            try:
                if i + 1 >= len(words):  # the number is the last word
                    tamyeez = None
                    tag = None
                else:
                    tamyeez = words[i + 1]

                if tamyeez:
                    _, tag = self.pos_tag(tamyeez)

                if tag and tag[0] in POS_Name_Tags:
                    gender = self.gender_detection_model(tamyeez)
                    # if the word is masculine, the number should be feminine
                    if gender == "male":
                        number = number2text(
                            original_numbers[ind],
                            feminine_flag=2,
                            grammar_pos_flag=grammar_flag,
                        )  # female
                    # if the word is feminine, the number should be masculine
                    else:
                        number = number2text(
                            original_numbers[ind],
                            feminine_flag=1,
                            grammar_pos_flag=grammar_flag,
                        )  # male
                else:
                    # the number is not name(NN),
                    # set the gender to default (male)
                    number = number2text(
                        original_numbers[ind],
                        feminine_flag=1,
                        grammar_pos_flag=grammar_flag,
                    )
            except Exception as e:
                number = number2text(
                    original_numbers[ind],
                    feminine_flag=1,
                    grammar_pos_flag=grammar_flag,
                )
            words[i] = number

        return " ".join(words)

    def pos_tag(self, text):
        pos_url = self.config.get("pos_url", None)
        try:
            if self.config["use_rpc"]:
                response = requests.post(url=pos_url, json={"text": text})
            else:
                response = g.call_microservice("post", url=pos_url, json={"text": text})

            assert response.status_code == 200
            result = response.json()
            words = [token["word"] for token in result["results"]]
            tags = [token["tag"] for token in result["results"]]

            return words, tags
        except Exception as e:
            logging.error(e)
            raise e

    def gender_detection_model(self, text):
        gender_detection_url = self.config.get("gender_detection_url", None)
        if not gender_detection_url:
            return text
        try:
            if self.config["use_rpc"]:
                r = requests.post(url=gender_detection_url, json={"text": text})
            else:
                r = g.call_microservice(
                    "post", url=gender_detection_url, json={"text": text}
                )

            result = r.json()
            gender_detection_res = result["results"]["gender"]
        except Exception as e:
            logging.log(e)
            return text
        return gender_detection_res
