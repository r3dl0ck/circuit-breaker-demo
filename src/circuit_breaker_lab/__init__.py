from flask import Flask
import os
import logging
import argparse
import time
from threading import Lock

logger = logging.getLogger(__name__)

app = Flask(__name__)

# Rate limiting variables
request_count = 0
last_request_time = 0.0
rate_limit_lock = Lock()
# RATE_LIMIT_PERIOD = 4  # seconds
# MAX_REQUESTS = 1


@app.route("/")
def hello():
    global request_count, last_request_time

    with rate_limit_lock:
        current_time = time.time()
        time_since_last_request = current_time - last_request_time

        if time_since_last_request > RATE_LIMIT_PERIOD:
            request_count = 0

        if request_count < MAX_REQUESTS:
            request_count += 1
            last_request_time = current_time
            return f"{MESSAGE}\n"
        else:
            return "Too many requests\n", 500


@app.route("/health")
def health():
    return "Healthy\n"


def main() -> None:
    parser = argparse.ArgumentParser(description='Circuit Breaker App')
    parser.add_argument('--flask-debug', dest='flask_debug', action='store_true',
                        help='Enable Flask debug mode')
    parser.add_argument('--no-flask-debug', dest='flask_debug', action='store_false',
                        help='Disable Flask debug mode')
    parser.set_defaults(flask_debug=os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't'])

    parser.add_argument('--flask-port', dest='flask_port', type=int,
                        default=int(os.getenv('FLASK_PORT', 8080)),
                        help='Port to run Flask app on')

    parser.add_argument('--host', dest='host', type=str,
                        default='0.0.0.0',
                        help='Host IP to listen on')

    parser.add_argument('--log-level', dest='log_level', type=str,
                        default=os.getenv('LOG_LEVEL', 'INFO').upper(),
                        help='Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')

    parser.add_argument('--rate-limit-period', dest='rate_limit_period', type=int,
                        default=int(os.getenv('RATE_LIMIT_PERIOD', 5)),
                        help='Rate limit period in seconds')

    parser.add_argument('--max-requests', dest='max_requests', type=int,
                        default=int(os.getenv('MAX_REQUEST', 1)),
                        help='Max requests allowed in rate limit period')

    parser.add_argument('--message', dest='message', type=str,
                        default="Hello World!",
                        help='Reply message')


    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=args.log_level)
    logger.info(f"Service starting up with args: {args}")

    global MAX_REQUESTS
    global RATE_LIMIT_PERIOD
    global MESSAGE
    MAX_REQUESTS = args.max_requests
    RATE_LIMIT_PERIOD = args.rate_limit_period
    MESSAGE = args.message

    app.run(host=args.host, port=args.flask_port, debug=args.flask_debug, use_reloader=False)
