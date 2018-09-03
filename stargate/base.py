import json
import logging
import importlib

import collections


class Startgate(object):
    """
        Collection of the Authentication action.
    """

    def __init__(self, app=None, environment=None):
        """

        :param app:
        :param environment:
        """
        self.app = app
        self.http = None
        # Register with application
        if app is not None:
            self.init_app(app, environment)

    def init_app(self, app=None, environment=None):
        pass


class StargateResponse(object):
    """
    Stargate response attribute
        :status_code:
        :body:
    """

    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])
