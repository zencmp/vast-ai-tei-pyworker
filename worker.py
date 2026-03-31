import os

from vastai import (
    Worker,
    WorkerConfig,
    HandlerConfig,
    BenchmarkConfig,
    LogActionConfig,
)

MODEL_SERVER_URL = "http://127.0.0.1"
MODEL_SERVER_PORT = int(os.environ.get("TEI_PORT", "8080"))
MODEL_LOG_FILE = os.environ.get("MODEL_LOG_FILE", "/workspace/tei.log")


def workload_calculator(payload):
    inputs = payload.get("inputs", "")
    if isinstance(inputs, list):
        return float(len(inputs)) * 100.0
    return 100.0


def embed_benchmark_generator():
    return {"inputs": "This is a benchmark sentence for measuring embedding throughput."}


worker_config = WorkerConfig(
    model_server_url=MODEL_SERVER_URL,
    model_server_port=MODEL_SERVER_PORT,
    model_log_file=MODEL_LOG_FILE,
    model_healthcheck_url="/health",
    handlers=[
        HandlerConfig(
            route="/embed",
            allow_parallel_requests=True,
            max_queue_time=60.0,
            workload_calculator=workload_calculator,
            benchmark_config=BenchmarkConfig(
                generator=embed_benchmark_generator,
                concurrency=5,
                runs=3,
            ),
        ),
    ],
    log_action_config=LogActionConfig(
        on_load=[
            "Ready",
            "Starting HTTP server",
        ],
        on_error=[
            "Error:",
            "Traceback (most recent call last):",
            "RuntimeError:",
        ],
        on_info=[
            "Downloading",
            "Fetching",
        ],
    ),
)

Worker(worker_config).run()
