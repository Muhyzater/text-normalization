import logging
import os
import sys
from concurrent import futures

import grpc
from flask import g
from grpc_health.v1.health import HealthServicer
from grpc_health.v1.health_pb2 import DESCRIPTOR as health_Descriptor
from grpc_health.v1.health_pb2_grpc import add_HealthServicer_to_server
from grpc_reflection.v1alpha import reflection
from micro_service import MicroService, Param, ParamSources, get_blueprint

import text_normalization.processing_pipeline as steps
import text_normalization.rpc as TN
from text_normalization.config import config, get_boolean, update_from_env

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

blueprint = get_blueprint()


def create_RPC_service(**kwargs):

    update_from_env(config)
    config.update(kwargs)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=config["workers"]))

    add_HealthServicer_to_server(HealthServicer(), server)

    text_normalization_servicer = TN.Servicer(config)

    TN.add_servicer(text_normalization_servicer, server)

    # set up connection
    server.add_insecure_port("0.0.0.0:{}".format(config["port"]))

    SERVICE_NAMES = (
        health_Descriptor.services_by_name["Health"].full_name,
        TN.Descriptor.services_by_name["text_normalization"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    return server


def create_REST_service(**kwargs):

    params = {}
    params.update(config)
    params.update(kwargs)

    microService = MicroService(__name__, **params)
    microService.config["use_rpc"] = False

    config.update(microService.config)
    microService.register_blueprint(blueprint)

    return microService


@blueprint.route(
    "/normalize_text",
    methods=["GET", "POST"],
    params=[
        Param(
            name="text",
            type=str,
            required=True,
            source=[ParamSources.ARGS, ParamSources.BODY_JSON],
        ),
        Param(
            name="advanced",
            type=bool,
            default=False,
            source=[ParamSources.ARGS, ParamSources.BODY_JSON],
        ),
        Param(
            name="parse_ssml",
            type=bool,
            default=False,
            source=[ParamSources.ARGS, ParamSources.BODY_JSON],
        ),
    ],
)
def normalize_text():
    p = g.params
    cfg = g.config
    try:

        pipeline = steps.DigitConversion()

        pipeline.set_next(steps.SSMLParsing(False)).set_next(
            steps.SplitText()
        ).set_next(steps.TreeWalking()).set_next(steps.NormalizeGenderPos()).set_next(
            steps.Packaging(False)
        )

        result = pipeline.process(p, cfg)

        return result.response, result.code, result.headers

    except Exception as _e:
        import traceback

        traceback.print_exc()

        return "FAIL", 500, cfg["headers"]


def run():

    if config["use_rpc"]:

        # starting gRPC server
        service = create_RPC_service()
        service.start()
        logging.info("started gRPC server on: {}".format(config["port"]))
        service.wait_for_termination()
    else:

        # starting Flask app
        service = create_REST_service()
        service.run_service()


if __name__ == "__main__":
    run()
