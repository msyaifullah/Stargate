import json
import collections


class TestUtils(object):

    def __init__(self):
        pass

    @staticmethod
    def string_to_ordered_dict(request_header, request_body):
        headers = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(request_header)
        body = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(request_body)

        return headers, body
