from functools import wraps
from traceback import print_exc
from types import FunctionType

import grpc


class AbortableRPC(type):
    """
    metaclass to wrap RPC methods seamlessly with graceful handling for
    server-side abortions
    """

    def __new__(cls, clsname: str, superclasses: tuple, attributedict: dict):

        # wrap methods
        superclass_attributes = [
            attr for attr in superclasses[0].__dict__ if not attr.startswith("_")
        ]

        for attr in superclass_attributes:
            # select RPC methods only
            if type(attributedict[attr]) is FunctionType:
                attributedict[attr] = cls.abortable(clsname, attributedict[attr])

        # adding attribute used in wrapper
        attributedict["testing"] = False

        return super(AbortableRPC, cls).__new__(
            cls, clsname, superclasses, attributedict
        )

    def abortable(servicer_cls, func):
        """
        decorator to gracefully handle aborts from RPC methods
        """

        @wraps(func)
        def wrapper(*args, **kwargs):

            try:
                context = None
                servicer = None

                CONTEXT_TYPE = grpc._server._Context

                for arg in args:
                    if arg.__class__.__name__ == servicer_cls:
                        servicer = arg
                        break

                assert servicer, "can't find servicer"

                if servicer.testing:
                    from grpc_testing._server import _servicer_context

                    CONTEXT_TYPE = _servicer_context.ServicerContext

                for arg in args:
                    if type(arg) is CONTEXT_TYPE:
                        context = arg
                        break

                assert context, "can't find context"

                return func(*args, **kwargs)

            except Exception as e:

                if context:
                    if context._state.aborted:
                        # server willingly aborted
                        raise
                    print_exc()
                    context.abort(
                        grpc.StatusCode.INTERNAL, "server got itself in trouble"
                    )
                else:
                    print_exc()
                    raise

        return wrapper


from .text_normalization_pb2 import DESCRIPTOR as Descriptor  # nopep8
from .text_normalization_pb2 import TNRequest, TNResponse  # nopep8
from .text_normalization_pb2_grpc import (
    add_text_normalizationServicer_to_server as add_servicer,
)  # nopep8
from .text_normalization_pb2_grpc import (
    text_normalizationServicer as BaseServicer,
)  # nopep8
from .text_normalization_pb2_grpc import text_normalizationStub as ClientStub  # nopep8
from .text_normalization_servicer import TNServicer as Servicer  # nopep8
