from flask import Flask
from controlers.api import Api
import logging
from controlers.orchestrator import Orchestrator

if __name__ == "__main__":
    app = Flask("__name__")
    logging.basicConfig(filename='api_server.log', level=logging.DEBUG)
    orchestrator = Orchestrator()
    api = Api(app, orchestrator)

    app.run(host='0.0.0.0', port=420)
