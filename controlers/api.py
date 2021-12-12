from flask import Flask

from controlers.orchestrator import Orchestrator


class Api:
    def __init__(self, app: Flask, orchestrator: Orchestrator):
        self.orchestrator = orchestrator
        self.app = app

        self.app.add_url_rule('/state', 'getState', self.get_state, methods=['GET'], )
        self.app.add_url_rule()

    def get_state(self):
        pass
