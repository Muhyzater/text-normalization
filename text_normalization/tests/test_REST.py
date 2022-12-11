import glob
import json
import unittest

import requests
from micro_service.micro_service_test_class import MicroServiceTestClass
from text_normalization.api import create_REST_service


class TextNormalizationRESTTest(MicroServiceTestClass):

    link = "http://localhost:5000/normalize_text"
    BASE = True
    ADV = True

    ssml_text = (
        "<speak>"
        '<say-as interpret-as="cardinal">123</say-as>'
        '<say-as interpret-as="ordinal">123</say-as>'
        '<say-as interpret-as="characters">abcd 123 ابجد</say-as>'
        '<say-as interpret-as="date">2/9/1666</say-as>'
        '<say-as interpret-as="phone">026398136</say-as>'
        '<say-as interpret-as="iban">JO94 CBJO 0010 0000 0000 0131 0003 02</say-as>'
        '<say-as interpret-as="currency">15.5 د.أ</say-as>'
        '<say-as interpret-as="time">21:35</say-as>'
        '<say-as interpret-as="unit">42 كغم</say-as>'
        "ذهب الولد"
        '<sub alias=" ذات مسؤولية محدودة"> ذ.م.م </sub>'
        "الى الحديقة"
        "</speak>"
    )

    ssml_result = (
        "<speak>"
        " مِئَةٌ وَثَلاثٌ وَعِشْرُونَ"
        " المِئَةُ وَالثالِثُ وَالعِشْرُونَ"
        " إِيه بِي سِي دِي واحَد اِثْنِين ثَلاثِة أَلِف باء جِيم دال"
        " الثانِي مِن أَيْلُولَ عامَ أَلْفٍ وَسِتِّمِئَةٍ وَسِتٍّ وَسِتِّينَ"
        " رَقْمُ صِفْر اِثْنانِ سِتَّةٌ ثَلاثَة تِسْعَة ثَمانِيَة واحِد ثَلاثَة سِتَّة"
        " جاي أَوْ تِسْعَةُ أَرْبَعَة سِي بِي جاي أَوْ صِفْر صِفْر"
        " واحِد صِفْر صِفْر صِفْر صِفْر صِفْر صِفْر صِفْر صِفْر صِفْر"
        " صِفْر واحِد ثَلاثَة واحِد صِفْر صِفْر صِفْر ثَلاثَة صِفْر اِثْنانِ"
        " خَمْسَ عَشْرَةَ دِينارٍ أُرْدُنِّيٍّ ﻭَخَمْسُونَ قُرْشَ"
        " التاسِعَةُ وَالنِصْفُ وَخَمْسُ دَقائِقَ مَساءَ"
        " إِثْنانٌ وَأَرْبَعُونَ كِيلُو غرام"
        " ذهب الولد"
        " ذات مسؤولية محدودة"
        " الى الحديقة"
        "</speak>"
    )

    @classmethod
    def setUpClass(self):
        """
        initiates a flask app test client before each test
        """
        app = create_REST_service(run=False)
        super(TextNormalizationRESTTest, self).setUpClass(
            app,
            title="Text Normalization Service",
            description=(
                "Given a text, write any numerical entities using textual format."
            ),
        )

        TEST_EXAMPLE_PATH = "text_normalization/tests/test_cases/test_case.*"
        self.test_cases = []
        for f_path in glob.glob(TEST_EXAMPLE_PATH):
            with open(f_path, "r") as f:
                try:

                    lines = [line.strip() for line in f.readlines()]
                    assert len(lines) == 3

                    input_text = lines[0]
                    normalized_text_basic = lines[1]
                    normalized_text_advanced = lines[2]

                except Exception:
                    print(f_path)
                    raise Exception

                test_case = {
                    "input_text": input_text,
                    "normalized_text_basic": normalized_text_basic,
                    "normalized_text_advanced": normalized_text_advanced,
                }
                self.test_cases.append(test_case)

    def test_base_mode(self):
        """
        Implements a test for a valid request to /normalize_text
        """
        if self.BASE:
            for test_case in self.test_cases:

                response = requests.post(
                    self.link, json={"text": test_case["input_text"], "advanced": False}
                )

                self.assertEqual(response.status_code, 200)

                returned_normalized_text = response.json()["results"]

                try:
                    self.assertEqual(
                        returned_normalized_text, test_case["normalized_text_basic"]
                    )
                except Exception as e:
                    print(e)
                    raise AssertionError

    # def test_advanced_mode(self):
    #     """
    #     Implements a test for a valid request to /normalize_text in advance
    #     mode
    #     """

    #     if self.ADV:
    #         for test_case in self.test_cases:
    #             response = requests.post(
    #                 self.link, json={"text": test_case["input_text"], "advanced": True}
    #             )

    #             self.assertEqual(response.status_code, 200)

    #             returned_normalized_text = response.json()["results"]
    #             try:
    #                 self.assertEqual(
    #                     returned_normalized_text, test_case["normalized_text_advanced"]
    #                 )
    #             except Exception as e:
    #                 print(e)
                    raise AssertionError

    def test_not_found_url(self):
        """Implements a test for a not-found-url request case"""
        response = requests.post(
            self.link + "x", json={"text": "ذهب الولد إلى الحديقة", "advanced": True}
        )
        self.assertEqual(response.status_code, 404)

    def test_bad_request(self):
        """Implements a test for a bad request case; missing 'text' field"""
        response = requests.post(self.link, json={"advanced": True})
        self.assertEqual(response.status_code, 400)

    # def test_ssml(self):
    #     """
    #     Implements a test for parsing SSML tags
    #     """

    #     response = requests.post(
    #         self.link, json={"text": self.ssml_text, "parse_ssml": True}
    #     )
    #     self.assertEqual(response.status_code, 200, response.content)
    #     self.assertEqual(response.json()["results"], self.ssml_result)

    #     # test invalid xml
    #     invalid_text = "<speak> </> </speak>"
    #     expected_error = "invalid SSML: bad XML"

    #     response = requests.post(
    #         self.link, json={"text": invalid_text, "parse_ssml": True}
    #     )
    #     self.assertEqual(response.status_code, 400, response.content)
    #     self.assertEqual(response.json()["results"], expected_error)

    #     # missing `interpret-as` attribute from `say-as` tag
    #     invalid_text = "<speak> <say-as>ذهب الولد للحديقة</say-as> </speak>"
    #     expected_error = "missing attribute 'interpret-as' from 'say-as' tag"

    #     response = requests.post(
    #         self.link, json={"text": invalid_text, "parse_ssml": True}
    #     )
    #     self.assertEqual(response.status_code, 400, response.content)
    #     self.assertEqual(response.json()["results"], expected_error)

    #     # invalid `interpret-as` attribute from `say-as` tag
    #     invalid_text = (
    #         '<speak> <say-as interpret-as="dummy">'
    #         "ذهب الولد للحديقة</say-as> </speak>"
    #     )
    #     expected_error = (
    #         "invalid 'interpret-as' attribute value: dummy. possible values"
    #     )

    #     response = requests.post(
    #         self.link, json={"text": invalid_text, "parse_ssml": True}
    #     )
    #     self.assertEqual(response.status_code, 400, response.content)
    #     self.assertIn(expected_error, response.json()["results"])

    #     # error handling `say-as` tag
    #     invalid_text = '<speak> <say-as interpret-as="characters"></say-as> </speak>'
    #     expected_error = "Error handling `say-as` tag:"

    #     response = requests.post(
    #         self.link, json={"text": invalid_text, "parse_ssml": True}
    #     )
    #     self.assertEqual(response.status_code, 400, response.content)
    #     self.assertIn(expected_error, response.json()["results"])

    def test_add_documentation(self):
        """run a test to add the OpenAPI docs"""

        response = requests.post(
            self.link,
            params={
                "text": "مساحة الشقة 80.3 م2 تقريباً",
                "advanced": False,
                "parse_ssml": False,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.add_documentation(response, description="Normalize text with all params")

        response = requests.post(
            self.link, params={"text": "مساحة الشقة 80.3 م2 تقريباً"}
        )
        self.assertEqual(response.status_code, 200)
        self.add_documentation(
            response, description="Normalize text with required only"
        )


if __name__ == "__main__":
    unittest.main()
