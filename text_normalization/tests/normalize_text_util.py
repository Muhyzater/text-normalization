import glob
import json
import sys

import requests
from pyarabic import araby


def normalize(f_path):
    """
    A flask app should be running before test
    """
    link = "http://localhost:5000/normalize_text"
    test_cases = []

    with open(f_path, "r") as f:
        lines = [line.strip() for line in f.readlines()]
        for line in lines:
            test_case = {
                "input_text": line,
                "unvoweled": araby.strip_tashkeel(line),
                "normalized_text_basic": "",
                "normalized_text_advanced": "",
            }
            test_cases.append(test_case)

    for test_case in test_cases:
        try:
            response = requests.post(
                link, json={"text": test_case["unvoweled"], "advanced": False}
            )
            test_case["normalized_text_basic"] = response.json()["results"]["text"]

        except Exception:
            raise Exception
        try:
            response = requests.post(
                link, json={"text": test_case["unvoweled"], "advanced": True}
            )
            test_case["normalized_text_advanced"] = response.json()["results"]["text"]
        except Exception:
            raise Exception
        print(test_case)
    f_output_path = open(f_path + ".normalized.txt", "w")
    for test_case in test_cases:
        f_output_path.write(
            test_case["normalized_text_basic"]
            + "\t"
            + test_case["normalized_text_advanced"]
            + "\n"
        )

    f_output_path.close()


if __name__ == "__main__":
    path = sys.argv[1]
    normalize(path)
