from flask import Flask, jsonify
import time

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter
)
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# Configure tracing
trace.set_tracer_provider(
    TracerProvider()
)

tracer = trace.get_tracer(__name__)

span_processor = BatchSpanProcessor(
    ConsoleSpanExporter()
)

trace.get_tracer_provider().add_span_processor(
    span_processor
)

app = Flask(__name__)

FlaskInstrumentor().instrument_app(app)

@app.route("/")
def home():

    with tracer.start_as_current_span(
        "home-request"
    ):

        time.sleep(1)

        return jsonify({
            "message": "Tracing Demo"
        })


@app.route("/payment")
def payment():

    with tracer.start_as_current_span(
        "payment-processing"
    ):

        time.sleep(2)

        return jsonify({
            "status": "Payment Successful"
        })


@app.route("/health")
def health():

    return jsonify({
        "status": "healthy"
    })


if __name__ == "__main__":
    app.run(debug=True)
