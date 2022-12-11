import re

from . import BaseStep, Processed, StatusCodeMapper


class Packaging(BaseStep):
    """
    Packaging the response
    """

    def __init__(self, use_rpc):
        self._code_mapper = StatusCodeMapper(use_rpc)

    def process(self, request: dict, config: dict):

        for sentence in request["sentences"]:
            sentence.text = re.sub(r" +", r" ", sentence.text)

        response = ". ".join([i.text for i in request["sentences"]])

        return Processed(response=response, code=self._code_mapper.OK, headers=None)
