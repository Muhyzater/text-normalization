import os
import re

url = "http://yjvhekp74bjkgexwxspeebfb47tqjc.staging.ingress.mawdu.com/{}"

config = dict(
    service_name="text_normalization",
    service_version="v4.1.10",
    environment="testing",
    workers=2,
    port=5000,
    file_log=True,
    DEBUG=False,
    suppress_logging=True,
    use_rpc={"default": False, "type": bool},
    pos_url={"default": url.format("ner-pos-segmentation-v1-2-3/pos"), "type": str},
    tashkeel_url={"default": url.format("tashkeel-v2-0-10/tashkeel"), "type": str},
    gender_detection_url={
        "default": url.format("gender-detection-v0-0-2/detect_gender"),
        "type": str,
    },
    threads_number={"default": 3, "type": int},
    model={"default": "tashkeel", "type": str},
)


def get_boolean(value) -> bool:
    t = re.compile(r"^(y|yes|true|on|1)$", re.IGNORECASE)
    f = re.compile(r"^(n|no|false|off|0)$", re.IGNORECASE)

    if t.match(str(value)):
        return True

    elif f.match(str(value)):
        return False

    else:
        raise ValueError("Invalid bool representation: '{}'".format(value))


def update_from_env(config: dict, prefix: str = "M3_", keys: list = None):

    for key in keys or config:

        if type(config[key]) is dict:
            _type = config[key]["type"]
            _default = config[key]["default"]

        else:
            _type = type(config[key])
            _default = config[key]

        config[key] = os.getenv("{}{}".format(prefix, key), _default)

        if _type is bool:
            config[key] = get_boolean(config[key])

        else:
            config[key] = _type(config[key])


update_from_env(config, keys=["use_rpc"])
