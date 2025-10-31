from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    SimpleSpanProcessor,
    ConsoleSpanExporter,
    BatchSpanProcessor,
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

def setup_tracer(service_name: str = "second_brain"):
    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

    # Optional: connect to OTEL Desktop Viewer
    try:
        otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)
        provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    except Exception:
        print("OTEL Desktop Viewer not running; using console exporter only.")

    trace.set_tracer_provider(provider)
    return trace.get_tracer(service_name)

# Global tracer
tracer = setup_tracer()