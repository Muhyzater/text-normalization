import glob
import io
import json
import logging
import threading
import time
from contextlib import redirect_stderr
from unittest import TestCase

import grpc
import requests
from text_normalization import rpc
from text_normalization.api import create_RPC_service

from .normalizer import TextNormalizer


class TextNormalizationgRPCTest(TestCase):

    port = 5001
    link = "0.0.0.0:{}".format(port)
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
        def run():

            service = create_RPC_service(port=self.port, use_rpc=True)
            service.start()
            logging.info("started gRPC server on: {}".format(self.port))
            service.wait_for_termination()

        self.server = threading.Thread(target=run)
        self.server.setDaemon(True)
        self.tester = TextNormalizer(self.link)

        f = io.StringIO()
        output = ""
        with redirect_stderr(f):
            self.server.start()
            for _ in range(10):
                output = f.getvalue()
                if "Running" in output:
                    break
                time.sleep(0.01)
        print(output)

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

        if self.BASE:
            for test_case in self.test_cases:
                response = self.tester.invoke(text=test_case["input_text"])
                self.assertEqual(response.code, grpc.StatusCode.OK)

                returned_normalized_text = response.response.text
                try:
                    self.assertEqual(
                        returned_normalized_text, test_case["normalized_text_basic"]
                    )
                except Exception as e:
                    print(e)
                    raise AssertionError

    def test_advanced_mode(self):

        if self.ADV:
            c = 0
            for test_case in self.test_cases:
                response = self.tester.invoke(
                    text=test_case["input_text"], advanced=True
                )
                self.assertEqual(response.code, grpc.StatusCode.OK)

                returned_normalized_text = response.response.text
                try:
                    self.assertEqual(
                        returned_normalized_text, test_case["normalized_text_advanced"]
                    )
                except Exception as e:
                    raise AssertionError

    # def test_ssml(self):
    #     """
    #     Implements a test for parsing SSML tags
    #     """

    #     response = self.tester.invoke(text=self.ssml_text, parse_ssml=True)

    #     self.assertEqual(response.code, grpc.StatusCode.OK, response.details)
    #     self.assertEqual(response.response.text, self.ssml_result)

    #     # test invalid xml
    #     invalid_text = "<speak> </> </speak>"
    #     expected_error = "invalid SSML: bad XML"

    #     response = self.tester.invoke(text=invalid_text, parse_ssml=True)
    #     self.assertEqual(response.code, grpc.StatusCode.INVALID_ARGUMENT)
    #     self.assertEqual(response.details, expected_error)

    #     # missing `interpret-as` attribute from `say-as` tag
    #     invalid_text = "<speak> <say-as>ذهب الولد للحديقة</say-as> </speak>"
    #     expected_error = "missing attribute 'interpret-as' from 'say-as' tag"

    #     response = self.tester.invoke(text=invalid_text, parse_ssml=True)
    #     self.assertEqual(response.code, grpc.StatusCode.INVALID_ARGUMENT)
    #     self.assertEqual(response.details, expected_error)

    #     # invalid `interpret-as` attribute from `say-as` tag
    #     invalid_text = (
    #         '<speak> <say-as interpret-as="dummy">'
    #         "ذهب الولد للحديقة</say-as> </speak>"
    #     )
    #     expected_error = (
    #         "invalid 'interpret-as' attribute value: dummy. possible values"
    #     )

    #     response = self.tester.invoke(text=invalid_text, parse_ssml=True)
    #     self.assertEqual(response.code, grpc.StatusCode.INVALID_ARGUMENT)
    #     self.assertIn(expected_error, response.details)

    #     # error handling `say-as` tag
    #     invalid_text = '<speak> <say-as interpret-as="characters"></say-as> </speak>'
    #     expected_error = "Error handling `say-as` tag:"

    #     response = self.tester.invoke(text=invalid_text, parse_ssml=True)
    #     self.assertEqual(response.code, grpc.StatusCode.INVALID_ARGUMENT)
    #     self.assertIn(expected_error, response.details)
