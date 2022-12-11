from collections import namedtuple

import grpc
from text_normalization import rpc

RpcResponse = namedtuple("RpcResponse", ["response", "code", "details"])


class TextNormalizer(object):
    def __init__(self, server_endpoint: str):

        channel = grpc.insecure_channel(server_endpoint)
        self.stub = rpc.ClientStub(channel)

    def invoke(self, **request_attributes: dict):

        request = rpc.TNRequest(**request_attributes)

        try:
            response = self.stub.normalize(request)
        except grpc.RpcError as error:
            return RpcResponse(None, error.code(), error.details())

        return RpcResponse(response, grpc.StatusCode.OK, None)
