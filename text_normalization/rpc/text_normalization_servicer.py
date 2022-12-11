import os
import sys

import grpc
import text_normalization.processing_pipeline as steps

from . import AbortableRPC, BaseServicer, TNRequest, TNResponse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TNServicer(BaseServicer, metaclass=AbortableRPC):
    def __init__(self, configs):

        self.configs = configs
        self.pipeline = steps.DigitConversion()
        self.pipeline.set_next(steps.SSMLParsing(True)).set_next(
            steps.SplitText()
        ).set_next(steps.TreeWalking()).set_next(steps.NormalizeGenderPos()).set_next(
            steps.Packaging(True)
        )

    def normalize(self, request: TNRequest, context):

        _request = dict(
            text=request.text, advanced=request.advanced, parse_ssml=request.parse_ssml
        )

        result = self.pipeline.process(_request, self.configs)

        if result.code != grpc.StatusCode.OK:
            context.abort(result.code, result.response)

        response = TNResponse(text=result.response)

        return response
