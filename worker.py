from pyworker import Worker, HandlerConfig, BenchmarkConfig
import os
import requests

TEI_PORT = int(os.getenv("TEI_PORT", "8080"))
TEI_HOST = os.getenv("TEI_HOST", "http://localhost")

def tei_handler(request):
    # Здесь проксируем запрос к TEI
    resp = requests.post(f"{TEI_HOST}:{TEI_PORT}/embed", json=request["inputs"], timeout=60)
    return resp.json()

config = Worker(
    handlers=[
        HandlerConfig(
            route="/embed",         
            handler=tei_handler,
            allow_parallel_requests=True,
        )
    ],
    benchmark=BenchmarkConfig(
        route="/embed",
        payload={"inputs": "This is a test sentence"},
        warmup=2,
        samples=10,
    ),
)

if __name__ == "__main__":
    Worker(config).run()
